<template>
  <section class="thread" :class="[locationClass, participantClass]" v-if="has_loaded">
    <div class="thread__header">
      <h2 v-if="location == 'home'" class="participant-header">
        <router-link
          :to="participantRoute">
          {{ people[participant].full_name }}
          <svg class="participant-header__symbol" width="13px" height="13px" viewBox="0 0 13 13" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
              <title>Arrow Top Right</title>
              <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g
                  class="icon-arrow-up-right"
                  fill="#000000"
                  fill-rule="nonzero"
                  stroke="#000000">
                      <g transform="translate(1.000000, 1.000000)">
                          <path d="M0.103329745,10.4696553 L9.87487302,0.698181818 L3.80599738,
                          0.698181818 C3.61320004,0.69818181 3.45690646,0.541888233 3.45690646,
                          0.349090909 C3.45690646,0.156293585 3.61320004,0 3.80599737,
                          0 L10.7175785,0 C10.9103758,-8.42747227e-09 11.0666694,
                          0.156293585 11.0666694,0.349090909 L11.0666694,7.26074182 C11.0666694,
                          7.45353914 10.9103758,7.60983273 10.7175784,7.60983273 C10.5247811,
                          7.60983273 10.3684875,7.45353914 10.3684875,7.26074182 L10.3684875,
                          1.19179636 L0.597014078,10.9633396 C0.46128405,11.1002636 0.24025365,
                          11.1012319 0.103329723,10.9655018 C-0.0335942042,
                          10.8297717 -0.0345625823,10.6087413 0.101167594,10.4718174 C0.101885136,
                          10.4710935 0.102605848,10.4703728 0.103329702,10.4696553 Z"></path>
                      </g>
                  </g>
              </g>
          </svg>
        </router-link>
      </h2>
      <h2 v-else class="participant-header">
        <router-link to="/">
          {{ people[participant].full_name }}
          <svg class="participant-header__symbol" width="11px" height="11px" viewBox="0 0 11 11" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
              <title>X</title>
              <g troke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                  <g
                    class="icon-x"
                    fill="#000000"
                    fill-rule="nonzero"
                    stroke="#000000">
                      <path d="M10.1592333,1.35923333 L6.01846667,5.5 L10.1592333,
                      9.64076667 C10.2981898,9.78463893 10.2962025,10.0133311 10.1547668,
                      10.1547668 C10.0133311,10.2962025 9.78463893,10.2981898 9.64076667,
                      10.1592333 L5.5,6.01846667 L1.35923333,10.1592333 C1.21536107,
                      10.2981898 0.986668915,10.2962025 0.845233189,10.1547668 C0.703797463,
                      10.0133311 0.70181019,9.78463893 0.840766667,9.64076667 L4.98153333,
                      5.5 L0.840766667,1.35923333 C0.745449252,1.26717269 0.707222048,
                      1.13084477 0.740777709,1.00264731 C0.774333371,0.874449856 0.874449856,
                      0.774333371 1.00264731,0.740777709 C1.13084477,0.707222048 1.26717269,
                      0.745449252 1.35923333,0.840766667 L5.5,4.98153333 L9.64076667,
                      0.840766667 C9.73282731,0.745449252 9.86915523,0.707222048 9.99735269,
                      0.740777709 C10.1255501,0.774333371 10.2256666,0.874449856 10.2592223,
                      1.00264731 C10.292778,1.13084477 10.2545507,1.26717269 10.1592333,
                      1.35923333 Z"></path>
                  </g>
              </g>
          </svg>
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

    <p v-if="used_cached" class="dev-only-message">
      <strong>[DEV ONLY] Cached Session Text...</strong><br />
      Please refresh in 60s to see changes!
    </p>

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
      .icon-chevron {
        fill: $color-akilah;
        stroke: $color-akilah;
      }
    }
    .icon-arrow-up-right,
    .icon-x {
      fill: $color-akilah;
      stroke: $color-akilah;
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
      .icon-chevron {
        fill: $color-robyn;
        stroke: $color-robyn;
      }
    }
    .icon-arrow-up-right,
    .icon-x {
      fill: $color-robyn;
      stroke: $color-robyn;
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
      .icon-chevron {
        fill: $color-timothy;
        stroke: $color-timothy;
      }
    }
    .icon-arrow-up-right,
    .icon-x {
      fill: $color-timothy;
      stroke: $color-timothy;
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

      .dev-only-message {
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