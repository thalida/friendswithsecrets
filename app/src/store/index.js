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
    defaultSession: 1,
    selectedParticipant: null,
    selectedSession: null,
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
    setThread(state, { participant, thread }) {
      Vue.set(state.threads, participant, thread);
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
    getAllPeople({ commit, state }, { participant, session }) {
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
          commit('setSelectedParticipant', participant);
          commit('setSelectedSession', session);
          commit('setIsLoading', { key: 'people', status: false });
        });
    },
    getThread({ commit, state }) {
      if (state.isLoading[state.selectedParticipant]) {
        return;
      }
      commit('setIsLoading', { key: state.selectedParticipant, status: true });
      const path = `${state.apiHost}/api/thread/${state.selectedParticipant}`;
      axios.get(path)
        .then((response) => {
          commit('setThread', {
            participant: state.selectedParticipant,
            thread: response.data,
          });
          commit('setIsLoading', { key: state.selectedParticipant, status: false });
        });
    },
    setSelected({ commit }, { participant, session }) {
      commit('setSelectedParticipant', participant);
      commit('setSelectedSession', session);
    },
  },
});
