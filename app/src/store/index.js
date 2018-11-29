import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);
const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  strict: debug,
  state: {
    apiHost: (process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '',
    isLoading: {},
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
    setIsLoading(state, { key, status }) {
      Vue.set(state.isLoading, key, status);
    },
    // not being used TODO: Remove
    setDefaultParticipant(state, participant) {
      state.defaultParticipant = participant;
    },
    setPeople(state, { people }) {
      Object.keys(people).map((key) => {
        const person = people[key];
        if (!person.is_therapist) {
          person.img_urls = {
            still: `/static/images/people/${person.name}.png`,
            moving: `/static/images/people/${person.name}.gif`,
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
        state.selectedSession = state.defaultSession;
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
          dispatch('setSelected', routeParams);
          commit('setIsLoading', { key: 'people', status: false });
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
      const sessionVal = (typeof participant === 'undefined') ? 1 : session;
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
