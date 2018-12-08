import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);
const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  strict: debug,
  state: {
    apiHost: (process.env.NODE_ENV === 'development') ? `http://${window.location.hostname}:5000` : '',
    localStorageKeys: {
      LAST_VISITED: 'last-visited',
      NUM_VISITS: 'num-visits',
    },
    isLoading: {},
    isFirstVisit: null,
    people: {},
    threads: {},
    participantOrder: [],
    defaultParticipant: null,
    defaultSession: null,
    selectedParticipant: null,
    selectedSession: null,
    selectedThread: null,
    nightModeKey: 'nightmode',
    nightMode: false,
    queryParams: {},
  },
  mutations: {
    setIsFirstVisit(state, status) {
      state.isFirstVisit = status;
    },
    setIsLoading(state, { key, status }) {
      Vue.set(state.isLoading, key, status);
    },
    setDefaultParticipant(state, participant) {
      state.defaultParticipant = participant;
    },
    setDefaultSession(state, session) {
      state.defaultSession = session;
    },
    setPeople(state, { people }) {
      Object.keys(people).map((key) => {
        const person = people[key];
        if (!person.is_therapist) {
          person.img_urls = {
            still: `/static/images/people/${person.name}.png?v=2`,
            moving: `/static/images/people/${person.name}.gif?v=2`,
          };
        }
        return person;
      });

      state.people = people;
    },
    setParticipantOrder(state, { participantOrder }) {
      state.participantOrder = participantOrder;
    },
    setThreads(state, { participant, thread }) {
      Vue.set(state.threads, participant, thread);
    },
    setSelectedThread(state, participant) {
      state.selectedThread = state.threads[participant];
    },
    setSelectedParticipant(state, participant) {
      if (typeof state.people[participant] !== 'undefined') {
        state.selectedParticipant = participant;
      } else {
        const randomIndex = Math.floor(Math.random() * state.participantOrder.length);
        state.selectedParticipant = state.participantOrder[randomIndex];
      }
    },
    setSelectedSession(state, session) {
      if (!isNaN(parseInt(session, 10))) {
        state.selectedSession = parseInt(session, 10);
      } else {
        state.selectedSession = null;
      }
    },
    setNightMode(state, value) {
      state.nightMode = value;
    },
    setQueryParams(state) {
      const params = {};

      if (state.nightMode) {
        params[state.nightModeKey] = null;
      }

      state.queryParams = params;
    },
  },
  actions: {
    newSiteVisit({ commit, state }) {
      let numVisits = 0;
      if (localStorage.getItem(state.localStorageKeys.NUM_VISITS)) {
        numVisits = localStorage.getItem(state.localStorageKeys.NUM_VISITS);
        numVisits = isNaN(numVisits) ? 0 : Math.abs(parseInt(numVisits, 10));
      }
      commit('setIsFirstVisit', numVisits === 0);
      localStorage.setItem(state.localStorageKeys.LAST_VISITED, new Date());
      localStorage.setItem(state.localStorageKeys.NUM_VISITS, numVisits + 1);
    },
    getAllPeople({ commit, state, dispatch }, routeParams) {
      if (state.isLoading.people) {
        return;
      }
      commit('setIsLoading', { key: 'people', status: true });
      const path = `${state.apiHost}/api/people`;
      axios.get(path)
        .then((response) => {
          const res = response.data;
          commit('setPeople', res);
          commit('setParticipantOrder', res);
          commit('setDefaultParticipant', res.participantOrder[0]);
          commit('setDefaultSession', null);
          dispatch('setSelected', routeParams).then(() => {
            dispatch('getAllThreads').then(() => {
              commit('setIsLoading', { key: 'people', status: false });
            });
          });
        });
    },
    getThread({ commit, state }, personKey) {
      const person = personKey || state.selectedParticipant;
      if (state.isLoading[person]) {
        return;
      }
      commit('setIsLoading', { key: person, status: true });
      const path = `${state.apiHost}/api/thread/${person}`;
      axios.get(path)
        .then((response) => {
          commit('setThreads', {
            participant: person,
            thread: response.data,
          });
          if (person === state.selectedParticipant) {
            commit('setSelectedThread', person);
          }
          commit('setIsLoading', { key: person, status: false });
        });
    },
    getAllThreads({ dispatch, state }) {
      dispatch('getThread', state.selectedParticipant);
      for (let i = 0; i < state.participantOrder.length; i += 1) {
        dispatch('getThread', state.participantOrder[i]);
      }
    },
    setSelected({ commit, state }, { participant, session }) {
      const sessionVal = (typeof participant === 'undefined') ? state.defaultSession : session;
      commit('setSelectedParticipant', participant);
      commit('setSelectedSession', sessionVal);
      commit('setSelectedThread', state.selectedParticipant);
    },
    setNightMode({ commit, state }, query) {
      const keyExists = typeof query[state.nightModeKey] !== 'undefined';

      if (!keyExists) {
        state.nightMode = false;
        return;
      }

      const value = query[state.nightModeKey];
      const isEnabled = value === null || value === 'true';
      commit('setNightMode', isEnabled);
      commit('setQueryParams');
    },
    toggleNightMode({ commit, state }) {
      commit('setNightMode', !state.nightMode);
      commit('setQueryParams');
    },
  },
});
