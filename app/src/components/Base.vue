<template>
  <div
    id="app"
    :class="[participantThreadClass]"
    v-if="isLoaded">
    <div id="body-gradient" class="body-gradient"></div>
    <Header />
    <div id="sticky-spacer"></div>
    <div class="slider-wrapper" :class="[{'is-loading': !areAllThreadsRendered}]">
      <tiny-slider
        ref="tinySlider"
        mode="carousel"
        items="1"
        :swipeAngle="10"
        :responsive="sliderResponsive"
        :controls="false"
        :nav="false"
        :loop="false"
        :startIndex="participantIndex">
        <Thread
          v-for="(person, index) in participantOrder"
          :key="index"
          v-bind:participant="person"
          v-bind:selectedSession="selectedSession"
          v-bind:is-thread-selected="selectedParticipant === person"
        />
      </tiny-slider>
    </div>
  </div>
</template>

<script>
import VueTinySlider from 'vue-tiny-slider';
import Header from './Header';
import People from './People';
import Thread from './Thread';

export default {
  name: 'Base',
  components: {
    'tiny-slider': VueTinySlider,
    Header,
    People,
    Thread,
  },
  data() {
    return {
      threadsRendered: [],
      $header: null,
      $headerGradient: null,
      $stickySpacer: null,
      $sliderInner: null,
      sliderResponsive: {
        800: {
          speed: 0,
        },
      },
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
    this.$root.$on('thread-rendered', this.onThreadRendered);
    this.$store.dispatch('newSiteVisit');
  },
  destroyed() {
    window.removeEventListener('scroll', this.onScroll);
    window.removeEventListener('resize', this.onResize);
  },
  watch: {
    $route(to) {
      this.$store.dispatch('setNightMode', to.query);
      this.$store.dispatch('setSelected', to.params).then(() => {
        this.$refs.tinySlider.goTo(this.participantIndex);
      });
    },
    nightMode(isEnabled) {
      const action = (isEnabled) ? 'add' : 'remove';
      document.body.classList[action]('nightmode');
    },
    areAllThreadsRendered(state) {
      if (state) {
        this.$refs.tinySlider.goTo(this.participantIndex);
        this.$refs.tinySlider.slider.events.on('indexChanged', this.onSliderIndexChanged);
      }
    },
  },
  computed: {
    isLoaded() {
      return this.$store.state.isLoading.people === false;
    },
    areAllThreadsRendered() {
      return this.threadsRendered.length === this.totalParticipants;
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
    onThreadRendered(participant) {
      this.updateSliderHeight();

      if (this.threadsRendered.indexOf(participant) >= 0) {
        return;
      }

      this.threadsRendered.push(participant);
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
    onSliderIndexChanged(data) {
      this.navigateToThread({
        participant: this.participantOrder[data.index],
        session: this.selectedSession,
      });
    },
    updateSliderHeight() {
      if (typeof this.$sliderInner === 'undefined' || this.$sliderInner === null) {
        this.$sliderInner = document.getElementsByClassName('tns-inner')[0];
      }

      const $slideWrapper = document.getElementsByClassName('thread--selected')[0];
      const $slideContents = $slideWrapper.getElementsByClassName('thread__sessions')[0];
      const slideBCR = $slideContents.getBoundingClientRect();
      let sliderHeight = null;
      if (slideBCR.height >= window.innerHeight - 60) {
        sliderHeight = slideBCR.height;
      } else {
        sliderHeight = window.innerHeight - 60;
      }
      this.$sliderInner.style.height = `${sliderHeight}px`;
      window.scrollTo(0, 0);
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

.slider-wrapper.is-loading {
  visibility:  hidden;
}

.tns-outer {
  overflow: hidden;
}

.tns-inner {
  min-height: 100%;
}

.tns-slider {
  display: flex;
  flex-direction: row;
  width: 100%;
  overflow: hidden;

  &.is-loading {
    visibility: hidden;
  }
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
  #app.thread--#{$person} {
    .person.person--#{$person} .name-image--still {
      display: none;
    }
    .person.person--#{$person} .name-image--moving {
      display: block;
    }
  }
}

body.nightmode {
  .body-gradient {
    background-image: linear-gradient($night-body-bg-color-light, $night-body-bg-color-dark);
  }
}

$fade-height-speed: 300ms;
.animation-fade-height-enter-active,
.animation-fade-height-leave-active {
  transition:
    max-height $fade-height-speed linear,
    opacity $fade-height-speed linear;
  max-height: 300px;
  opacity: 1;
  overflow: hidden;
}
.animation-fade-height-enter,
.animation-fade-height-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
