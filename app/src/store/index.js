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
  },
  mutations: {
    setIsLoading(state, { key, status }) {
      Vue.set(state.isLoading, key, status);
    },
    setDefaultParticipant(state, participant) {
      state.defaultParticipant = participant;
    },
    setPeople(state, { people }) {
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
        state.selectedParticipant = state.defaultParticipant;
      }
    },
    setSelectedSession(state, session) {
      if (!isNaN(parseInt(session, 10))) {
        state.selectedSession = parseInt(session, 10);
      } else {
        state.selectedSession = state.defaultSession;
      }
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
  },
});
