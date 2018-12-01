<template>
  <header id="header" class="header" :class="{
    'is-open': headerIsOpen,
    'is-closed': !headerIsOpen
  }" data-sticky>
      <div id="header__gradient" class="header__gradient"></div>
      <a
        tabindex="0"
        class="header__btn header__btn--theme"
        v-on:click="toggleNightMode()"
        v-on:keyup.enter="toggleNightMode()"
        :title="'Turn ' + (nightModeEnabled ? 'off' : 'on') + ' night mode'">
          <img v-if="nightModeEnabled" src="/static/images/day-icon.svg" />
          <img v-else src="/static/images/night-icon.svg" />
      </a>
      <a
        tabindex="0"
        class="header__btn header__btn--about-toggle"
        v-on:click="toggle()"
        v-on:keyup.enter="toggle()"
        :title="(headerIsOpen ? 'Close' : 'Open') + ' about section'">
          <img v-if="!headerIsOpen" src="/static/images/question.svg" />
          <img v-else src="/static/images/x.svg" />
      </a>
      <transition name="animation-fade-height">
        <div class="header__about container-wrapper" v-show="headerIsOpen">
            <img class="logo" src="/static/images/fws-logo.gif?v=1" />
            <p class="header__about__text">
              Three friends with different backgrounds participated in online
              text therapy sessions from January to April 2018.
              Friends With Secrets captures a slice of their lives — the good, the bad,
              the heartbreaking — and how they try to process the world around them.
              This is a refinement of 5 sessions.
              The identities of the therapists have been protected.
            </p>
            <div class="header__about__credits">
                <p class="header__about__credit">
                  Project by
                  <a href="https://twitter.com/AkilahObviously" target="_blank">Akilah Hughes</a>,
                  <a href="https://twitter.com/robynkanner" target="_blank">Robyn Kanner</a>,
                  and <a href="https://www.instagram.com/timothygoodman/" target="_blank">Timothy Goodman</a>
                </p>
                <p class="header__about__credit">
                  Code by <a href="http://thalida.codes/" target="_blank">Thalida Noel</a>
                </p>
                <p class="header__about__credit">
                  Web Design by Robyn Kanner and Timothy Goodman
                </p>
                <p class="header__about__credit">
                  Logo by <a href="https://john-sampson.com/" target="_blank">John Sampson</a>
                </p>
                <p class="header__about__credit">
                  Photo by <a href="https://www.justindoesthings.com/" target="_blank">Justin J. Wee</a>
                </p>
                <p class="header__about__credit">
                  For inquires
                  <a href="mailto:friendswithsecrets@gmail.com">friendswithsecrets@gmail.com</a>
                </p>
            </div>
            <img class="header__about__photo" src="/static/images/people/fws_group.jpg?v=2" />
        </div>
      </transition>
      <People />
  </header>
</template>

<script>
import People from './People';

export default {
  name: 'Header',
  components: {
    People,
  },
  data() {
    return {
      headerIsOpen: false,
      // headerIsOpen: this.$store.state.isFirstVisit,
    };
  },
  watch: {
    $route() {
      this.headerIsOpen = false;
    },
  },
  computed: {
    queryParams() {
      return this.$store.state.queryParams;
    },
    selectedParticipant() {
      return this.$store.state.selectedParticipant;
    },
    selectedSession() {
      return this.$store.state.selectedSession;
    },
    nightModeEnabled() {
      return this.$store.state.nightMode;
    },
  },
  methods: {
    toggle() {
      this.headerIsOpen = !this.headerIsOpen;

      if (this.headerIsOpen) {
        window.scrollTo(0, 0);
      }
    },
    toggleNightMode() {
      this.$store.dispatch('toggleNightMode');
      this.$router.push({
        name: 'Thread',
        params: {
          participant: this.selectedParticipant,
          session: this.selectedSession,
        },
        query: this.queryParams,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../assets/styles/toolkit';
.header {
  display: block;
  position: relative;
  width: 100%;
  overflow: hidden;
  min-height: 60px;

  .logo {
    display: block;
    margin-bottom: 20px;
    width: 80%;
    margin: 0 auto;
  }

  &__gradient {
    display: none;
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: -1;
    background-image: linear-gradient($body-bg-color-light, $body-bg-color-dark);
    background-repeat: no-repeat;
    background-attachment: fixed;
  }

  &__btn {
    $margin: 15px;
    display: flex;
    position: absolute;
    cursor: pointer;
    margin: 0;
    height: 35px;
    width: 35px;
    background: white;
    border-radius: 50%;

    justify-content: center;
    align-items: center;

    &--about-toggle {
      top: $margin;
      right: $margin;
    }

    &--theme {
      top: $margin;
      left: $margin;
    }
  }

  &__about {
      position: relative;
      height: auto;
      margin-top: 50px;

      a {
          color: $text-color;
      }

      &__text,
      &__credits {
          display: block;
          position: relative;
          width: 48%;
          float: left;
          font-size: 16px;
          line-height: 1.5;
          margin: 0;
          padding: 0;
      }

      &__credits {
          margin: 0 0 0 2%;
      }

      &__credit {
        line-height: 1.5;
        margin: 0;
        padding: 0;
      }

      &__photo {
        width: 100%;
        margin: 30px 0;
      }

      &:after {
          content: "";
          display: table;
          clear: both;
      }
  }

  &.is-open {
    align-items: flex-start;
  }

  &.is-sticky {
    .header__gradient { display: block; }
  }

  @media screen and (max-width: 800px), screen and (max-height: 400px) {
    .logo {
      width: 100%;
    }

    &__about {
      min-width: 90%;
      &__text,
      &__credits {
          display: block;
          float: none;
          width: 100%;
          margin: 0 0 20px 0;
      }
    }
  }
}

.nightmode {
  .header__gradient {
    background-image: linear-gradient($night-body-bg-color-light, $night-body-bg-color-dark);
  }

  .header__about,
  .header__about a {
    color: $night-color-light;
  }
}
</style>
