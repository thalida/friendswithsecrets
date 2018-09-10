<template>
<section class="thread container-wrapper" v-show="isLoaded">
  <transition-group
    name="animation-fade"
    tag="ol"
    class="thread__sessions"
    v-scroll-to:params="{isLoaded, selectedSession: selectedSessionZeroIdx}"
    v-height:params="{isLoaded, windowHeight}">
    <Session
      v-for="(session, index) in threadSessions"
      :key="index"
      v-bind:index="index"
      v-bind:session="session"
      v-bind:session-number="getSessionNumber(index)"
      v-bind:people="people"
      v-bind:selected="index === selectedSessionZeroIdx"
      v-on:session-toggle="onSessionToggle" />
  </transition-group>
</section>
</template>

<script>
import Session from './Session';

export default {
  name: 'Thread',
  components: {
    Session,
  },
  data() {
    return {
      windowHeight: this.getViewportSize().height,
    };
  },
  created() {
    this.$store.dispatch('getAllThreads');
  },
  mounted() {
    window.addEventListener('resize', this.onResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
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
    height: {
      update(elem, args) {
        if (!args.value.isLoaded) {
          return;
        }

        const $el = elem;
        const params = args.value;
        $el.style.height = `${params.windowHeight - $el.getBoundingClientRect().y}px`;
      },
    },
    scrollTo: {
      update(elem, args) {
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
        $el.scrollTop = toggleHeight * params.selectedSession;
      },
    },
  },
  methods: {
    getOuterHeight($el) {
      const styles = window.getComputedStyle($el);
      const margin = parseFloat(styles.marginTop) + parseFloat(styles.marginBottom);
      return Math.ceil($el.offsetHeight + margin);
    },
    getViewportSize() {
      let $el = window;
      let prefix = 'inner';

      if (!('innerWidth' in window)) {
        $el = document.documentElement || document.body;
        prefix = 'client';
      }

      const width = $el[`${prefix}Width`];
      const height = $el[`${prefix}Height`];
      return { width, height };
    },
    setWindowHeight() {
      const viewport = this.getViewportSize();
      this.windowHeight = viewport.height;
    },
    getSessionNumber(index) {
      const pad = (index + 1 < 10) ? '0' : '';
      return `${pad}${index + 1}`;
    },
    onSessionToggle(e) {
      this.$root.$emit('session-select', {
        participant: this.selectedParticipant,
        session: (e.state === true) ? e.index : null,
      });
    },
    onResize() {
      this.setWindowHeight();
    },
  },
};
</script>

<style lang="scss">
@import '../assets/styles/toolkit';
.thread {
  overflow: hidden;

  .dev-only-message {
    display: none;
    font-size: 12px;
    text-align: center;
  }

  &__sessions {
    width: 100%;
    overflow: auto;
    padding: 0 0 10% 0;
  }
}
</style>
