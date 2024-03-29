<template>
<section
  class="thread"
  v-bind:class="{ 'thread--animated': swipe.isAnimating }"
  v-bind:style="{ transform: swipeTransformStyles }"
  v-show="isLoaded"
  v-scroll-to:params="{isLoaded, selectedSession: selectedSessionZeroIdx}">
  <ol class="thread__sessions container-wrapper">
    <Session
      v-for="(session, index) in threadSessions"
      :key="index"
      v-bind:index="index"
      v-bind:session="session"
      v-bind:people="people"
      v-bind:selected="index === selectedSessionZeroIdx"
      v-on:session-toggle="onSessionToggle" />
    </ol>
</section>
</template>

<script>
import interact from 'interactjs';
import Session from './Session';

export default {
  name: 'Thread',
  components: {
    Session,
  },
  data() {
    return {
      swipeTransformStyles: null,
      swipe: {
        LEFT: 0,
        RIGHT: 1,
        NEUTRAL: null,
        isEnabled: false, // vp.width < 800,
        isAnimating: false,
        direction: null, // left = 0 | right = 1 | neutral = null
        x: 0,
        threshold: 20,
      },
    };
  },
  created() {
    this.$store.dispatch('getAllThreads');
  },
  mounted() {
    const self = this;
    interact(this.$el).draggable({
      enabled: self.swipe.isEnabled,
      autoScroll: true,
      inertia: true,
      onstart() {
        self.swipe.isAnimating = true;
      },
      onmove(event) {
        const x = (self.swipe.x || 0) + event.dx;
        self.swipe.x = x;
        self.swipeTransformStyles = `translate(${self.swipe.x}px, 0)`;
      },
      onend() {
        self.swipe.isAnimating = false;
        // eslint-disable-next-line
        // console.log('got in here', self.swipe.x);
        if (self.swipe.x > self.swipe.threshold) {
          self.swipe.direction = self.swipe.RIGHT;
        } else if (self.swipe.x < -self.swipe.threshold) {
          self.swipe.direction = self.swipe.LEFT;
        } else {
          self.swipe.direction = self.swipe.NEUTRAL;
          self.swipe.x = 0;
        }

        self.onSwipeEnd();
      },
    });
  },
  beforeDestroy() {
    interact(this.$el).unset();
  },
  computed: {
    selectedParticipant() {
      return this.$store.state.selectedParticipant;
    },
    selectedSession() {
      return this.$store.state.selectedSession;
    },
    selectedSessionZeroIdx() {
      return this.selectedSession - 1;
    },
    participantOrder() {
      return this.$store.state.participantOrder;
    },
    selectedParticipantIndex() {
      return this.participantOrder.indexOf(this.selectedParticipant);
    },
    people() {
      return this.$store.state.people;
    },
    isLoaded() {
      return this.$store.state.isLoading[this.selectedParticipant] === false;
    },
    threadData() {
      return this.$store.state.selectedThread;
    },
    threadSessions() {
      return (this.threadData) ? this.threadData.sessions : [];
    },
  },
  directives: {
    scrollTo: {
      componentUpdated(elem, args) {
        if (!args.value.isLoaded) {
          return;
        }

        const $el = elem;
        const params = args.value;
        const $sessionToggle = $el.querySelector('.session__toggle');

        if ($sessionToggle === null) {
          return;
        }

        const styles = window.getComputedStyle($sessionToggle);
        const margin = parseFloat(styles.marginTop) + parseFloat(styles.marginBottom);
        const toggleHeight = Math.ceil($sessionToggle.offsetHeight + margin);
        window.scrollTo(0, toggleHeight * params.selectedSession);
      },
    },
  },
  methods: {
    onSessionToggle(e) {
      if (this.swipe.isAnimating) {
        return;
      }
      this.$root.$emit('session-select', {
        participant: this.selectedParticipant,
        session: (e.state === true) ? e.index : null,
      });
    },
    onSwipeEnd() {
      if (this.swipe.direction === null) {
        this.swipeTransformStyles = 'translate(0, 0)';
        return;
      }

      const shift = (this.swipe.direction === this.swipe.LEFT) ? 1 : -1;
      const participant = this.participantOrder[(this.selectedParticipantIndex + shift)] || null;

      this.swipe.direction = this.swipe.NEUTRAL;
      this.swipe.isAnimating = false;
      this.swipe.x = 0;
      this.swipeTransformStyles = 'translate(0, 0)';

      if (participant === null) {
        return;
      }

      this.$root.$emit('navigate', {
        participant,
        session: this.selectedSession,
      });
    },
  },
};
</script>

<style lang="scss">
@import '../assets/styles/toolkit';
.thread {
  display: block;
  position: relative;
  width: 100%;
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;

  .dev-only-message {
    display: none;
    font-size: 12px;
    text-align: center;
  }

  &__sessions {
    padding: 0 0 60px 0;
  }

  &--animated {
    position: absolute;
    transition: all 100ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
}
</style>
