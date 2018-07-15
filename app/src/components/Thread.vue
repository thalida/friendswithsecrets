<template>
  <section class="thread" :class="[locationClass, participantClass]" v-if="has_loaded">
    <div class="thread__header">
      <h2 v-if="location == 'home'" class="participant-header">
        <router-link
          :to="participantRoute">
          {{ people[participant].full_name }}
          <span class="participant-header__symbol">-></span>
        </router-link>
      </h2>
      <h2 v-else class="participant-header">
        <router-link to="/">
          {{ people[participant].full_name }}
          <span class="participant-header__symbol">x</span>
        </router-link>
      </h2>

      <select
        class="participant-dropdown"
        v-model="selectedParticipant"
        v-on:change="onParticipantSelect">
        <option
          v-for="(name, index) in allParticipants"
          :key="index"
          :value="name">
            {{name}}
        </option>
      </select>

      <select
        class="sessions-dropdown"
        v-model="selectedSession"
        v-on:change="onSessionSelect">
        <option value="" v-if="location === 'home'">sessions</option>
        <option
          v-for="(session, index) in sessions"
          :key="index"
          :value="index">
            {{ getSessionNumber(index) }}. session
        </option>
      </select>
    </div>

    <div
      class="thread__sessions"
      v-scroll-to:params="{isMobile, selectedSession}"
      v-height:params="{location, windowHeight}">
      <Session
        v-for="(session, index) in sessions"
        :key="index"
        v-bind:index="index"
        v-bind:session="session"
        v-bind:session-number="getSessionNumber(index)"
        v-bind:people="people"
        v-bind:selected="index === selectedSession"
        v-on:session-toggle="onSessionToggle" />
    </div>
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
  props: {
    participant: String,
    location: {
      type: String,
      default() {
        return 'standalone';
      },
    },
    viewSession: {
      type: Number,
      default() {
        return 1;
      },
    },
  },
  data() {
    const isMobile = this.setIsMobile();
    return {
      isMobile,
      has_loaded: false,
      apiHost: (process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '',
      allParticipants: ['akilah', 'robyn', 'timothy'],
      selectedParticipant: this.participant,
      selectedSession: (this.location === 'home' && isMobile) ? '' : this.viewSession - 1,
      lastSelectedSession: null,
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
    participantClass() {
      return `thread--${this.participant}`;
    },
    participantRoute() {
      return {
        name: 'Thread',
        params: {
          participant: this.participant,
          viewSession: this.selectedSession + 1,
        },
      };
    },
    locationClass() {
      return `thread--${this.location}`;
    },
  },
  watch: {
    $route(to, from) {
      if (to.params.participant !== from.params.participant) {
        this.has_loaded = false;
        this.selectedParticipant = to.params.participant;
        this.selectedSession = to.params.viewSession - 1;
        this.getThreadData();
      }
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

        if (params.isMobile) {
          return;
        }

        const $sessionToggle = $el.querySelector('.session__toggle');
        const styles = window.getComputedStyle($sessionToggle);
        const margin = parseFloat(styles.marginTop) + parseFloat(styles.marginBottom);
        const toggleHeight = Math.ceil($sessionToggle.offsetHeight + margin);
        $el.scrollTop = toggleHeight * params.selectedSession;
      },
      update(elem, args) {
        const $el = elem;
        const params = args.value;

        if (params.isMobile) {
          return;
        }

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
    setIsMobile() {
      const viewport = this.getViewportSize();
      this.isMobile = viewport.width <= 700 || viewport.height <= 400;
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
      const path = `${this.apiHost}/api/thread/${this.participant}`;
      axios.get(path)
        .then((response) => {
          this.sessions = response.data.sessions;
          this.people[response.data.participant.name] = response.data.participant;
          this.people[response.data.therapist.name] = response.data.therapist;
          this.has_loaded = true;
        });
    },
    onParticipantSelect() {
      this.$router.push({
        name: 'Thread',
        params: {
          participant: this.selectedParticipant,
          viewSession: this.selectedSession + 1,
        },
      });
    },
    onSessionToggle(e) {
      if (e.state === true) {
        this.selectedSession = (e.state === true) ? e.index : this.selectedSession;
        this.emitSessionSelect();
        if (this.location === 'standalone') {
          this.$router.push({
            name: 'Thread',
            params: {
              participant: this.participant,
              viewSession: this.selectedSession + 1,
            },
          });
        }
      }
    },
    onSessionSelect() {
      this.emitSessionSelect();
      this.$router.push({
        name: 'Thread',
        params: {
          participant: this.participant,
          viewSession: this.selectedSession + 1,
        },
      });
    },
    onResize() {
      this.setIsMobile();
      this.setWindowHeight();
    },
    emitSessionSelect() {
      this.$root.$emit('session-select', {
        participant: this.participant,
        selectedSession: this.selectedSession,
      });
    },
  },
};
</script>

<style lang="scss">
@import '../assets/styles/colors';
.thread {
  position: relative;
  overflow: hidden;

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

    font-weight: bold;
    font-size: 48px;
    text-align: center;
    text-transform: lowercase;
    vertical-align: middle;

    a {
      text-decoration: none;
    }
  }

  .participant-dropdown {
    display: inline-block;
    vertical-align: sub;
    background: #FFFFFF;
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
    background: #FFFFFF;
    width: 128px;
    padding: 5px 0;
    font-size: 14px;
    border: 0;
    border-radius: 0;
    border-bottom: 2px solid #222222;
  }

  &--home {
    $total-threads: 3;
    $width: 100% / $total-threads;
    $padding: 10%;
    $padding-adjustment: ($padding / 2) / $total-threads;

    float: left;
    margin-top: $padding / 2;

    .thread__sessions {
      border-right: 1px solid $color-gray;
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

  &--akilah {
    .participant-dropdown,
    .participant-header,
    .participant-header a {
      color: $color-akilah;
    }
    .message--akilah .message__text {
      background-color: $color-akilah;
    }
    .session--expanded .session__toggle {
      border-color: $color-akilah;
    }
  }

  &--robyn {
    .participant-dropdown,
    .participant-header,
    .participant-header a {
      color: $color-robyn;
    }
    .message--robyn .message__text {
      background-color: $color-robyn;
    }
    .session--expanded .session__toggle {
      border-color: $color-robyn;
    }
  }

  &--timothy {
    .participant-dropdown,
    .participant-header,
    .participant-header a {
      color: $color-timothy;
    }
    .message--timothy .message__text {
      background-color: $color-timothy;
    }
    .session--expanded .session__toggle {
      border-color: $color-timothy;
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

      .thread__sessions {
        display: none;
      }
    }

    &--standalone {
      width: 80%;

      .participant-header{
        display: none;
      }
      .participant-dropdown {
        display: block;
        float: left;
      }
      .sessions-dropdown {
        display: block;
        float: right;
        margin: 15px 0;
      }
      .session__toggle,
      .session.session--collapsed {
        display: none;
      }
    }
  }
}
</style>
