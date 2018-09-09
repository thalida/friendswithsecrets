<template>
  <section class="thread" v-if="has_loaded">
    <p v-if="used_cached" class="dev-only-message">
      <strong>[DEV ONLY] Cached Session Text...</strong><br />
      Please refresh in 60s to see changes!
    </p>

    <ol
      class="thread__sessions"
      v-scroll-to:params="{selectedSession}"
      v-height:params="{windowHeight}">
      <Session
        v-for="(session, index) in sessions"
        :key="index"
        v-bind:index="index"
        v-bind:session="session"
        v-bind:session-number="getSessionNumber(index)"
        v-bind:people="people"
        v-bind:selected="index === selectedSession"
        v-on:session-toggle="onSessionToggle" />
    </ol>
  </section>
</template>

<script>
import axios from 'axios';
import Session from './Session';

export default {
  name: 'Thread',
  components: {
    Session,
  },
  data() {
    return {
      has_loaded: false,
      apiHost: (process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '',
      defaultParticipant: 'akilah',
      defaultSession: 1,
      used_cached: false,
      sessions: [],
      people: {},
      windowHeight: this.getViewportSize().height,
    };
  },
  created() {
    this.getThreadData();
  },
  mounted() {
    window.addEventListener('resize', this.onResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  computed: {
    selectedParticipant() {
      return this.$route.params.participant || this.defaultParticipant;
    },
    selectedSession() {
      const session = this.$route.params.session || this.defaultSession;
      return session - 1;
    },
  },
  watch: {
    $route(to, from) {
      if (from.params.participant === to.params.participant) {
        return;
      }

      this.has_loaded = false;
      this.getThreadData();
    },
  },
  directives: {
    height: {
      inserted(elem, args) {
        const $el = elem;
        const params = args.value;
        $el.style.height = `${params.windowHeight - $el.getBoundingClientRect().y}px`;
      },
      update(elem, args) {
        const $el = elem;
        const params = args.value;
        $el.style.height = `${params.windowHeight - $el.getBoundingClientRect().y}px`;
      },
    },
    scrollTo: {
      inserted(elem, args) {
        const $el = elem;
        const params = args.value;
        const $sessionToggle = $el.querySelector('.session__toggle');
        const styles = window.getComputedStyle($sessionToggle);
        const margin = parseFloat(styles.marginTop) + parseFloat(styles.marginBottom);
        const toggleHeight = Math.ceil($sessionToggle.offsetHeight + margin);
        $el.scrollTop = toggleHeight * params.selectedSession;
      },
      update(elem, args) {
        const $el = elem;
        const params = args.value;
        const $sessionToggle = $el.querySelector('.session__toggle');
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
    getThreadData() {
      const path = `${this.apiHost}/api/thread/${this.selectedParticipant}`;
      axios.get(path)
        .then((response) => {
          const res = response.data;
          this.setThreadData(res);
        });
    },
    setThreadData(res) {
      this.sessions = res.sessions;
      this.people[res.participant.name] = res.participant;
      this.people[res.therapist.name] = res.therapist;
      this.used_cached = res.used_cached;
      this.has_loaded = true;
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
@import '../assets/styles/colors';
.thread {
  position: relative;
  overflow: hidden;

  .dev-only-message {
    font-size: 12px;
    text-align: center;
  }

  &__header {
    width: 100%;
    height: 64px;

    &:after {
      content: "";
      clear: both;
      display: table;
    }
  }

  &__sessions {
    width: 100%;
    overflow: auto;
    padding: 0 0 10% 0;
  }

  .participant-header {
    margin: 10px 0;

    color: $text-color;
    font-weight: bold;
    font-size: 48px;
    text-align: center;
    text-transform: lowercase;
    vertical-align: middle;

    a {
      text-decoration: none;
    }

    &__symbol {
      vertical-align: middle;
    }
  }

  .participant-dropdown {
    display: inline-block;
    vertical-align: sub;
    background: $body-bg-color;
    color: $text-color;
    padding: 5px 0;
    font-size: 36px;
    font-family: 'Dosis', sans-serif;
    margin: 0;
    border: 0;
    border-radius: 0;
  }

  .sessions-dropdown {
    display: inline-block;
    vertical-align: sub;
    background: $body-bg-color;
    color: $text-color;
    width: 128px;
    padding: 5px 0;
    font-size: 14px;
    border: 0;
    border-radius: 0;
    border-bottom: 2px solid $text-color;
  }

  .icon-x {
    fill: $text-color;
    stroke: $text-color;
  }

  &--home {
    $total-threads: 3;
    $width: 100% / $total-threads;
    $padding: 10%;
    $padding-adjustment: ($padding / 2) / $total-threads;

    float: left;
    margin-top: $padding / 2;

    .thread__sessions {
      border-right: 2px solid $color-gray-2;
    }

    .participant-dropdown {
      display: none;
    }

    .sessions-dropdown {
      display: none;
    }

    &:nth-child(1) {
      width: $width - ($padding-adjustment - ($padding-adjustment / 4));
      .thread__sessions {
        padding-left: 0;
        padding-right: $padding;
      }
    }

    &:nth-child(2) {
      width: $width + ($padding-adjustment + ($padding-adjustment / 2));
      .thread__sessions {
        padding-left: $padding;
        padding-right: $padding;
      }
    }

    &:nth-child(3) {
      width: $width - ($padding-adjustment - ($padding-adjustment / 4));
      .thread__sessions {
        padding-left: $padding;
        padding-right: 0;

        border-right: 0;
      }
    }
  }

  &--standalone {
    width: 80%;
    max-width: 800px;
    margin: 0 auto;

    .participant-dropdown {
      display: none;
    }

    .sessions-dropdown {
      display: none;
    }
  }

  @media screen and (max-width: 700px), screen and (max-height: 400px) {
    .participant-header__symbol {
      display: none;
    }

    &--home,
    &--standalone {
      float: none;
      margin: 0 auto;
    }

    &--home {
      width: 100% !important;
      height: auto;
      overflow: hidden;

      .thread__header {
        height: auto;
      }

      .participant-header {
        display: inline-block;
        font-size: 36px;
        margin: 0;
      }

      .sessions-dropdown {
        display: inline-block;
      }

      .thread__sessions,
      .dev-only-message {
        display: none;
      }
    }

    &--standalone {
      width: 80%;

      .participant-dropdown {
        display: block;
        float: left;
      }
      .sessions-dropdown {
        display: block;
        float: right;
        margin: 15px 0;
      }

      .participant-header,
      .session__toggle,
      .session.session--collapsed {
        display: none;
      }
    }
  }
}
</style>
