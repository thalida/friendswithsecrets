<template>
  <div
    id="app"
    :class="[participantThreadClass]"
    v-if="isLoaded">
    <Header />
    <div id="sticky-spacer"></div>
    <div
      :class="{
        'is-header-open': headerIsOpen,
        'content-nightmode': nightModeEnabled,
        'content-daymode': !nightModeEnabled
      }">
      <router-view />
    </div>
  </div>
</template>

<script>
import Header from './Header';
import People from './People';
import Thread from './Thread';

export default {
  name: 'Base',
  components: {
    Header,
    People,
    Thread,
  },
  data() {
    return {
      $header: null,
      $stickySpacer: null,
      runningOnScroll: false,
      headerIsOpen: false,
      nightModeEnabled: false,
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
  },
  mounted() {
    this.$root.$on('session-select', this.onSessionSelect);
    this.$root.$on('navigate', this.navigateToThread);
    this.$root.$on('thread-rendered', this.onThreadRendered);
    this.$root.$on('header-toggled', this.onHeaderToggled);
    this.$store.dispatch('newSiteVisit');
  },
  destroyed() {
    window.removeEventListener('scroll', this.onScroll);
  },
  watch: {
    $route(to) {
      this.$store.dispatch('setNightMode', to.query);
      this.$store.dispatch('setSelected', to.params);
    },
    nightMode(isEnabled) {
      const action = (isEnabled) ? 'add' : 'remove';
      document.body.classList[action]('nightmode');
      this.nightModeEnabled = isEnabled;
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
    participantThreadClass() {
      return `thread--${this.selectedParticipant}`;
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
    onHeaderToggled(state) {
      this.headerIsOpen = state;
    },
    onScroll() {
      this.updateStickyHeader();
    },
    updateStickyHeader() {
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
        this.$stickySpacer.style.height = `${headerBoundingClientRect.height}px`;
      } else {
        this.$stickySpacer.style.height = '0px';
      }

      this.runningOnScroll = false;
    },
    onSessionSelect(data) {
      const participant = data.participant;
      const session = !isNaN(parseInt(data.session, 10)) ? data.session + 1 : null;
      this.navigateToThread({ participant, session });
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

  height: 100%;
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;

  font: normal normal 16px/1.2 'proxima-nova', sans-serif;
  color: $text-color;
  background-color: $body-bg-color-dark;

  &.nightmode {
    background-color: $night-body-bg-color-dark;
  }
}

#app {
  display: block;
  position: relative;
  height: 100%;
}

.content-daymode,
.content-nightmode {
  position: relative;
  &.is-header-open::before {
    position: absolute;
  }
}

.content-daymode {
  &::before {
    content: ' ';
    position: fixed; // instead of background-attachment
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background-color: $body-bg-color-dark;
    background-image: linear-gradient(to bottom, $body-bg-color-light 0%, $body-bg-color-dark 100%);
    background-repeat: no-repeat;
    background-size: cover;
    will-change: transform; // creates a new paint layer
    z-index: -1;
  }
}

.content-nightmode {
  &::before {
    content: ' ';
    position: fixed; // instead of background-attachment
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background-color: $night-body-bg-color-dark;
    background-image: linear-gradient(
      to bottom,
      $night-body-bg-color-light 0%,
      $night-body-bg-color-dark 100%
    );
    background-repeat: no-repeat;
    background-size: cover;
    will-change: transform; // creates a new paint layer
    z-index: -1;
  }
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

$fade-height-speed: 300ms;
.animation-fade-height-enter-active,
.animation-fade-height-leave-active {
  transition:
    max-height $fade-height-speed linear,
    opacity $fade-height-speed linear;
  max-height: 800px;
  opacity: 1;
  overflow: hidden;
}
.animation-fade-height-enter,
.animation-fade-height-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
