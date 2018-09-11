<template>
  <div id="app" :class="[participantThemeClass]" v-if="isLoaded">
    <Header />
    <div class="people container-wrapper">
      <span
        class="person"
        :class="['person--' + participant]"
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
          {{ people[participant].full_name }}
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
    const isValidPerson = ['akilah', 'timothy', 'robyn'].includes(to.params.participant);
    const isEmptyPerson = typeof to.params.participant === 'undefined';
    if (!isValidPerson && !isEmptyPerson) {
      next('/');
      return;
    }

    next();
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
    people() {
      return this.$store.state.people;
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
@import '../assets/styles/toolkit';

html {
  box-sizing: border-box;
}

*, *:before, *:after {
  box-sizing: inherit;
}

body {
  margin: 0;
  padding: 0;
  font: normal normal 16px/1.2 'proxima-nova', sans-serif;
  color: $text-color;
  background: linear-gradient($color-gray-3, $color-gray-2);
  height: 100%;
}

html,
body,
#app {
  height: 100%;
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

.container-wrapper {
  display: block;
  margin: 0 auto;
  width: 80%;
  max-width: 800px;
}

.people {
  display: block;
  position: relative;
  z-index: 1;
  box-shadow: 0px 4px 8px -8px #000;
}

.person {
  display: inline-block;
  width: 33%;
  margin: 32px 0;
  text-align: center;
  font-weight: bold;
  font-size: 38px;
  color: #222;

  &:first-child {
    text-align: left;
  }

  &:last-child {
    text-align: right;
  }

  &_link {
    text-decoration: none;
    transition: color 400ms ease;
  }
}

.animation-fade-enter-active,
.animation-fade-leave-active {
  transition: opacity 300ms ease;
}
.animation-fade-enter,
.animation-fade-leave-to {
  opacity: 0;
}


@each $person in $people {
  .theme--#{$person} {
    .header,
    .message--#{$person}.message--participant .message__text,
    .session--expanded .session__toggle,
    .session--collapsed .session__toggle {
       @extend %bg-color--#{$person};
    }
    .person--#{$person} .person_link {
       @extend %color--#{$person};
    }
    .session--expanded .session__toggle__contents {
       @extend %bg-color--faded--#{$person};
    }
  }
}
</style>
