<template>
  <header class="header">
      <a
        tabindex="0"
        class="header__btn"
        v-on:click="toggle()"
        v-on:keyup.enter="toggle()"
        :title="(headerIsOpen ? 'Close' : 'Open') + ' about section'">
          <span v-if="!headerIsOpen">?</span>
          <span v-else>X</span>
      </a>
      <transition name="animation-fade-height">
          <div class="header__about container-wrapper" v-if="headerIsOpen">
              <p class="header__about__text">
                Three friends from different backgrounds participated in 10
                individual online text therapy sessions from January to April 2018.
                Friends With Secrets captures a slice of their lives
                — the good and the bad — including identity, feelings,
                and how they try to process the world around them.
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
                    Design by
                    <a href="https://twitter.com/robynkanner" target="_blank">Robyn Kanner</a>
                    and <a href="https://www.instagram.com/timothygoodman/" target="_blank">Timothy Goodman</a>
                  </p>
                  <p class="header__about__credit">
                    Code by <a href="http://thalida.codes/" target="_blank">Thalida Noel</a>
                  </p>
                  <p class="header__about__credit">
                    For inquires email us at
                    <a href="mailto:friendswithsecrets@gmail.com">friendswithsecrets@gmail.com</a>
                  </p>
              </div>
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
  methods: {
    toggle() {
      this.headerIsOpen = !this.headerIsOpen;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../assets/styles/toolkit';
.header {
  display: flex;
  align-items: flex-end;
  flex-direction: column;
  width: 100%;

  &__btn {
      display: block;
      // float: right;
      width: 30px;
      height: 30px;
      margin: 15px;
      padding: 5px 0;
      cursor: pointer;
      border-radius: 50%;
      background: #FFFFFF;
      text-align: center;
  }

  &__about {
      position: relative;
      height: auto;

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

      &:after {
          content: "";
          display: table;
          clear: both;
      }
  }

  @media screen and (max-width: 800px), screen and (max-height: 400px) {
    align-items: center;
    flex-flow: row-reverse wrap;

    .people {
      margin-left: 5%;
      width: calc(85% - 30px);
    }

    &__btn {
      margin-right: 5%;
    }

    &__about {
      order: 1;
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
</style>
