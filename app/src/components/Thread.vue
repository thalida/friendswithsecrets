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
    <div class="thread__sessions">
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
    const isDesktop = window.innerWidth > 600;
    return {
      has_loaded: false,
      apiHost: (process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '',
      allParticipants: ['akilah', 'robyn', 'timothy'],
      selectedParticipant: this.participant,
      selectedSession: (this.location === 'home' && !isDesktop) ? '' : this.viewSession - 1,
      lastSelectedSession: null,
      sessions: [],
      people: {},
    };
  },
  created() {
    this.getThreadData();
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
  methods: {
    getOuterHeight($el) {
      const styles = window.getComputedStyle($el);
      const margin = parseFloat(styles.marginTop) + parseFloat(styles.marginBottom);
      return Math.ceil($el.offsetHeight + margin);
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

        const $scrollContainer = this.$el.querySelector('.thread__sessions');
        const $sessionToggle = $scrollContainer.querySelector('.session__toggle');
        const toggleHeight = this.getOuterHeight($sessionToggle);
        $scrollContainer.scrollTop = toggleHeight * this.selectedSession;
      }
    },
    onSessionSelect() {
      this.$router.push({
        name: 'Thread',
        params: {
          participant: this.participant,
          viewSession: this.selectedSession + 1,
        },
      });
    },
  },
};
</script>

<style lang="scss">
$color-gray: #EEE;
$color-akilah: #40DCFB;
$color-robyn: #65FFF6;
$color-timothy: #18E5EA;

.thread {
  position: relative;
  overflow: hidden;

  &__header {
    width: 100%;
    &:after {
      content: "";
      clear: both;
      display: table;
    }
  }

  &__sessions {
    width: 100%;
    height: 300px;
    overflow: auto;
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

    width: $width;
    float: left;
    margin-top: 60px;

    .thread__sessions {
      border-right: 1px solid $color-gray;
      padding: 0;
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

    .thread__sessions {
      padding: 0;
    }

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

  @media screen and (max-width: 700px), screen and (max-height: 500px) {
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
