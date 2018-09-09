<template>
  <div id="app" v-if="isLoaded">
    <Header />
    <div class="people">
      <span
        class="person"
        :key="index"
        v-for="(participant, index) in participantOrder">
        <router-link
          class="person_link"
          :to="{
            name: 'Thread',
            params: {
              participant: participant,
              session: selectedSession,
            }
          }"
        >
          {{ participant }}
          <!-- {{ people[participant].full_name }} -->
        </router-link>
      </span>
    </div>
    <router-view />
  </div>
</template>

<script>
import Header from './Header';

export default {
  name: 'Base',
  components: {
    Header,
  },
  data() {
    return {};
  },
  beforeRouteEnter(to, from, next) {
    if (['akilah', 'timothy', 'robyn'].includes(to.params.participant)
      || typeof to.params.participant === 'undefined') {
      next();
    }

    next('/');
  },
  created() {
    this.$store.dispatch('getAllPeople', this.$route.params);
  },
  mounted() {
    this.$root.$on('session-select', this.onSessionSelect);
  },
  watch: {
    $route(to) {
      this.$store.dispatch('setSelected', to.params);
    },
  },
  computed: {
    isLoaded() {
      return this.$store.state.isLoading.people === false;
    },
    participantOrder() {
      return this.$store.state.participantOrder;
    },
    selectedParticipant() {
      return this.$store.state.selectedParticipant;
    },
    selectedSession() {
      return this.$store.state.selectedSession;
    },
    participantThemeClass() {
      return `theme--${this.selectedParticipant}`;
    },
  },
  methods: {
    onSessionSelect(data) {
      const session = !isNaN(parseInt(data.session, 10)) ? data.session + 1 : null;
      this.$router.push({
        name: 'Thread',
        params: {
          participant: data.participant,
          session,
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

.people {
  display: block;
  width: 80%;
  margin: 0 auto;
}

.person {
  display: inline-block;
  width: 33%;
  text-align: center;

  &:first-child {
    text-align: left;
  }

  &:last-child {
    text-align: right;
  }

  &_link {
    text-decoration: none;
  }
}
</style>
