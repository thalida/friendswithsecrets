<template>
  <div
    id="app"
    :class="[participantThemeClass, {'nightmode': nightMode}]"
    v-if="isLoaded">
    <Header />
    <router-view />
  </div>
</template>

<script>
import Header from './Header';
import People from './People';

export default {
  name: 'Base',
  components: {
    Header,
    People,
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
    this.$store.dispatch('setNightMode', this.$route.query);
    this.$store.dispatch('getAllPeople', this.$route.params);
  },
  mounted() {
    this.$root.$on('session-select', this.onSessionSelect);
    this.$root.$on('navigate', this.navigateToThread);
  },
  watch: {
    $route(to) {
      this.$store.dispatch('setNightMode', to.query);
      this.$store.dispatch('setSelected', to.params);
    },
  },
  computed: {
    isLoaded() {
      return this.$store.state.isLoading.people === false;
    },
    queryParams() {
      return this.$store.state.queryParams;
    },
    people() {
      return this.$store.state.people;
    },
    nightMode() {
      return this.$store.state.nightMode;
    },
    participantOrder() {
      return this.$store.state.participantOrder;
    },
    participantIndex() {
      return this.participantOrder.indexOf(this.selectedParticipant);
    },
    totalParticipants() {
      return this.participantOrder.length;
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
    navigateToThread({ participant, session }) {
      this.$router.push({
        name: 'Thread',
        params: {
          participant,
          session,
        },
        query: this.queryParams,
      });
    },
    onSessionSelect(data) {
      const participant = data.participant;
      const session = !isNaN(parseInt(data.session, 10)) ? data.session + 1 : null;
      this.navigateToThread({ participant, session });
    },
    onSwipe(directionStr) {
      if (directionStr !== 'left' && directionStr !== 'right') {
        return;
      }

      const direction = (directionStr === 'left') ? 1 : -1;
      const participant = this.participantOrder[(this.participantIndex + direction)] || null;

      if (participant === null) {
        return;
      }

      this.navigateToThread({ participant, session: this.selectedSession });
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
  height: 100%;
  overflow: hidden;
}

html,
body,
#app {
  height: 100%;
}

#app {
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
  background: $body-bg-color;
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
  width: 90%;
  max-width: 800px;
}

.text--uppercase {
  text-transform: uppercase;
}

@each $person in $people {
  .theme--#{$person} {
    .message--#{$person}.message--participant .message__text {
      @extend %bg-color--#{$person};
      color: $text-color-light;
    }
    .person--#{$person} .person_link {
       @extend %color--#{$person};
    }
    .session--expanded {
      .session__toggle {
        @extend %bg-color--#{$person};
      }
    }
  }
}

#app.nightmode {
  background: $night-body-bg-color;

  @each $person in $people {
    &.theme--#{$person} {
      .message--#{$person}.message--participant .message__text {
        background-color: $night-name-color;
        color: $text-color-light;
      }
      .person--#{$person} .person_link {
        color: $night-name-color;
      }
      .session--expanded {
        .session__toggle {
          background-color: $night-name-color;
        }
      }
    }
  }
}

.animation-fade-enter-active,
.animation-fade-leave-active {
  transition: opacity 400ms ease;
}
.animation-fade-enter,
.animation-fade-leave-to {
  opacity: 0;
}

.animation-height-enter-active,
.animation-height-leave-active {
  transition: max-height 400ms ease-in-out;
  max-height: 300px;
  overflow: hidden;
}
.animation-height-enter,
.animation-height-leave-to {
  max-height: 0;
}

$fade-height-1x-speed: 400ms;
$fade-height-2x-speed: $fade-height-1x-speed / 2;

.animation-fade-height-enter-active,
.animation-fade-height-leave-active {
  transition:
    max-height $fade-height-1x-speed ease-in-out,
    opacity $fade-height-1x-speed ease-in-out;
  max-height: 300px;
  opacity: 1;
  overflow: hidden;
}
.animation-fade-height-enter,
.animation-fade-height-leave-to {
  max-height: 0;
  opacity: 0;
}

.animation--fade-height--2x-enter-active,
.animation--fade-height--2x-leave-active {
  transition:
    max-height $fade-height-2x-speed ease-in-out,
    opacity $fade-height-2x-speed ease-in-out;
  max-height: 300px;
  opacity: 1;
  overflow: hidden;
}
.animation--fade-height--2x-enter,
.animation--fade-height--2x-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
