<template>
  <header id="header" class="header" :class="{
    'is-open': headerIsOpen,
    'is-closed': !headerIsOpen
  }" data-sticky>
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
            <img class="logo" src="/static/images/fws-logo.gif?v=3" />
            <p class="header__about__text">
              Three friends with different backgrounds participated in online
              text therapy sessions from January to April 2018.
              Friends With Secrets captures a slice of their lives — the good, the bad,
              the heartbreaking — and how they try to process the world around them.
              The sessions have been refined.
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
                  Logo Design by <a href="https://john-sampson.com/" target="_blank">John Sampson</a>
                </p>
                <p class="header__about__credit">
                  Photo by <a href="https://www.justindoesthings.com/" target="_blank">Justin J. Wee</a>
                </p>
                <p class="header__about__credit">
                  For inquires
                  <a href="mailto:hi@friendswithsecrets.com">hi@friendswithsecrets.com</a>
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
      this.$root.$emit('header-toggled', this.headerIsOpen);

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
  background-color: $body-bg-color-light;

  .logo {
    display: block;
    margin-bottom: 20px;
    width: 85%;
    margin: 0 auto 10px;
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

  &.is-closed {}

  @media screen and (max-width: 800px), screen and (max-height: 400px) {
    .logo {
      width: 104%;
      margin-left: -2%;
    }

    &__btn {
      width: 30px;
      height: 30px;
    }

    &__about {
      min-width: 90%;
      margin-top: 60px;

      &__text,
      &__credits {
          display: block;
          float: none;
          width: 100%;
          margin: 0 0 20px 0;
      }

      &__text {
          margin: 0 0 20px 0;
      }

      &__credits {
          margin: 0;
      }
    }
  }
}

.nightmode {
  .header {
    background-color: $night-body-bg-color-light;
  }

  .header__about,
  .header__about a {
    color: $night-color-light;
  }
}
</style>
