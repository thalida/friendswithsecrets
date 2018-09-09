<template>
  <div id="app">
    <Header />
    <router-link
      v-for="(participant, index) in participantOrder"
      :key="index"
      :to="{ name: 'Thread', params: {
        participant: participant,
        session: selectedSession + 1
      }}">
      {{ participant }}
      <!-- {{ people[participant].full_name }} -->
    </router-link>
    <router-view />
  </div>
</template>

<script>
import Header from './Header';
// import Thread from './Thread';

export default {
  name: 'Base',
  components: {
    Header,
  },
  data() {
    return {
      participantOrder: ['akilah', 'robyn', 'timothy'],
      defaultParticipant: 'akilah',
      defaultSession: 1,
      people: {},
    };
  },
  created() {
    this.$session.start();
  },
  mounted() {
    this.$root.$on('session-select', this.onSessionSelect);
  },
  computed: {
    selectedParticipant() {
      return this.$route.params.participant || this.defaultParticipant;
    },
    selectedSession() {
      const session = this.$route.params.session || this.defaultSession;
      return session - 1;
    },
    participantThemeClass() {
      return `theme--${this.selectedParticipant}`;
    },
  },
  methods: {
    onSessionSelect(data) {
      this.$router.push({
        name: 'Thread',
        params: {
          participant: data.participant,
          session: data.session + 1,
        },
      });
    },
  },
};
</script>

<style lang="scss">
@import '../assets/styles/colors';
html {
  box-sizing: border-box;
}

*, *:before, *:after {
  box-sizing: inherit;
}

body {
  background-color: $body-bg-color;
  margin: 0;
  padding: 0;
  font: 16px/1.2 'Dosis', sans-serif;
  color: $text-color;
}

a {
  color: $text-color;
}

ol {
  padding: 0;
  margin: 0;
  list-style-type: none;
}

li {
  list-style: none;
}
</style>
