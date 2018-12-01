<template>
  <div
    id="app"
    :class="[participantThemeClass]"
    v-if="isLoaded">
    <div id="body-gradient" class="body-gradient"></div>
    <Header />
    <div id="sticky-spacer"></div>
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
    return {
      $header: null,
      $headerGradient: null,
      $stickySpacer: null,
    };
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
    window.addEventListener('scroll', this.onScroll);
    window.addEventListener('resize', this.onResize);
  },
  mounted() {
    this.$root.$on('session-select', this.onSessionSelect);
    this.$root.$on('navigate', this.navigateToThread);
    this.$store.dispatch('newSiteVisit');
  },
  destroyed() {
    window.removeEventListener('scroll', this.onScroll);
    window.removeEventListener('resize', this.onResize);
  },
  watch: {
    $route(to) {
      this.$store.dispatch('setNightMode', to.query);
      this.$store.dispatch('setSelected', to.params);
    },
    nightMode(isEnabled) {
      const action = (isEnabled) ? 'add' : 'remove';
      document.body.classList[action]('nightmode');
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
    onScroll() {
      if (typeof this.$header === 'undefined' || this.$header === null) {
        this.$header = document.getElementById('header');
      }

      if (typeof this.$stickySpacer === 'undefined' || this.$stickySpacer === null) {
        this.$stickySpacer = document.getElementById('sticky-spacer');
      }

      const headerBoundingClientRect = this.$header.getBoundingClientRect();
      const headerOffset = this.$header.offsetTop;
      const action = (
        !this.$header.classList.contains('is-open')
        && window.pageYOffset > headerOffset
      ) ? 'add' : 'remove';

      this.$header.classList[action]('is-sticky');
      if (action === 'add') {
        this.onResize();
        this.$stickySpacer.style.height = `${headerBoundingClientRect.height}px`;
      } else {
        this.$stickySpacer.style.height = '0px';
      }
    },
    onResize() {
      if (typeof this.$headerGradient === 'undefined' || this.$headerGradient === null) {
        this.$headerGradient = document.getElementById('header__gradient');
      }

      const windowHeight = window.innerHeight
        || document.documentElement.clientHeight
        || document.body.clientHeight;
      document.body.style.height = `${windowHeight}px`;
      this.$headerGradient.style.height = `${windowHeight}px`;
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
  height: 100%;
  box-sizing: border-box;
}

*, *:before, *:after {
  box-sizing: inherit;
}

body {
  margin: 0;
  padding: 0;

  height: 100%;
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;

  font: normal normal 16px/1.2 'proxima-nova', sans-serif;
  color: $text-color;
}

.body-gradient {
  display: block;
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -1;
  background-image: linear-gradient($body-bg-color-light, $body-bg-color-dark);
  background-repeat: no-repeat;
  background-attachment: fixed;
}

#app {
  display: block;
  position: relative;
  height: auto;
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

.is-sticky {
  position: fixed !important;
  z-index: 1;
}

#sticky-spacer {
  display: block;
  position: relative;
  width: 100%;
  height: 0px;
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
    .person.person--#{$person} .name-image--still {
      display: none;
    }
    .person.person--#{$person} .name-image--moving {
      display: block;
    }
    .session--expanded {
      .session__toggle {
        @extend %bg-color--#{$person};
      }
    }
  }
}

body.nightmode {
  .body-gradient {
    background-image: linear-gradient($night-body-bg-color-light, $night-body-bg-color-dark);
  }

  @each $person in $people {
    #app.theme--#{$person} {
      .message--#{$person}.message--participant .message__text {
        background-color: $night-color-dark;
        color: $text-color-light;
      }
      .person--#{$person} .person_link {
        color: $night-color-light;
      }
      .session--expanded {
        .session__toggle {
          background-color: $night-color-dark;
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

$fade-height-1x-speed: 300ms;
$fade-height-2x-speed: $fade-height-1x-speed / 2;

.animation-fade-height-enter-active,
.animation-fade-height-leave-active {
  transition:
    max-height $fade-height-1x-speed linear,
    opacity $fade-height-1x-speed linear;
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
