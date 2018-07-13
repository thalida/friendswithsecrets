<template>
  <div>
    <Header v-if="location === 'standalone'" v-bind:location="'thread'" />
    <section class="thread" :class="[locationClass, participantClass]" v-if="has_loaded">
      <div class="thread__header">
        <h2 class="participant-header">
          {{ people[participant].full_name }}
          <span class="participant-header__symbol">
            <router-link v-if="location == 'home'" :to="participantRoute">--></router-link>
            <router-link v-else to="/">x</router-link>
          </span>
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
      <Session
        v-for="(session, index) in sessions"
        :key="index"
        v-bind:index="index"
        v-bind:session="session"
        v-bind:session-number="getSessionNumber(index)"
        v-bind:people="people"
        v-bind:selected="index === selectedSession" />
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import Header from './Header';
import Session from './Session';

export default {
  name: 'Thread',
  components: {
    Header,
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
  methods: {
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
          viewSession: 1,
        },
      });
    },
    onSessionSelect() {
      if (this.location === 'home') {
        this.$router.push({
          name: 'Thread',
          params: {
            participant: this.participant,
            viewSession: this.selectedSession + 1,
          },
        });
      }
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

  &__header {
    width: 100%;
    &:after {
      content: "";
      clear: both;
      display: table;
    }
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

  &:last-child .session {
    border-right: 0;
  }

  &--home {
    width: 33%;
    float: left;
    height: 80vh;
    overflow: auto;
    margin-top: 60px;

    .session:first-child {
      margin-top: 300px;
    }

    .session {
      padding: 0px 30px;
    }

    .participant-dropdown {
      display: none;
    }

    .sessions-dropdown {
      display: none;
    }
  }

  &--standalone {
    width: 80%;
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

  @media screen and (max-width: 600px) {
    .participant-header__symbol {
      display: none;
    }

    &--home,
    &--standalone {
      width: 80%;
      float: none;
      margin: 0 auto;
    }

    &--home {
      .participant-header {
        display: inline-block;
        font-size: 36px;
        margin: 0;
      }

      .session {
        display: none;
      }

      .sessions-dropdown {
        display: inline-block;
      }
    }

    &--standalone {
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
