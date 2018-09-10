<template>
  <header class="header">
      <div class="header__bar container-wrapper">
          <router-link to="/" class="header__link">Friends with Secrets</router-link>
          <a
            tabindex="0"
            class="header__btn"
            v-on:click="toggle()"
            v-on:keyup.enter="toggle()"
            :title="(headerIsOpen ? 'Close' : 'Open') + ' about section'">
              <span
                v-if="!headerIsOpen">?</span>
              <span
                v-else>X</span>
          </a>
      </div>
      <div class="header__body" v-if="headerIsOpen">
          <p class="header__body__about header__body__about--inline">
              Three friends participated in 15 individual online text therapy
              sessions from January to April 2018. These sessions capture a slice
              of their life, their thoughts and feelings, their individualitiies,
              and how they try to process the world around them. The identities of
              the therapists have been protected.
          </p>
          <div class="header__body__credits">
              <p class="header__body__credit">
                  project by <a href="#">Akilah Hughes</a>,
                  <a href="#">Robyn Kanner</a>, <a href="#">Timothy Goodman</a>
              </p>
              <p class="header__body__credit">
                  website coded by <a href="#">Thalida Noel</a>
              </p>
              <p class="header__body__credit">
                  for inquires email us at <a href="#">FriendsWithSecrets@gmail.com</a>
              </p>
          </div>
      </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
    location: String,
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
  display: block;
  position: relative;
  width: 100%;
  min-height: 64px;
  padding: 15px 0;

  &__bar {
      display: block;
      margin: 0 auto;
      width: 80%;

      &:after {
          content: "";
          clear: both;
          display: table;
      }
  }

  &__link {
      display: inline-block;
      margin: 5px 0;
      padding: 0;
      font: bold 18px/1.2 'PT Sans', sans-serif;
      vertical-align: middle;
      text-decoration: none;
  }

  &__btn {
      display: inline-block;
      float: right;
      width: 30px;
      padding: 5px 0;
      cursor: pointer;
      border-radius: 50%;
      background: #FFFFFF;
      text-align: center;
  }

  &__body {
      display: block;
      width: 80%;
      margin: 0 auto;
      position: relative;
      height: auto;

      p {
          margin: 0;
          padding: 0;
      }

      a {
          color: $text-color;
      }

      &__about,
      &__credits {
          display: block;
          position: relative;
          width: 48%;
          float: left;
          text-transform: lowercase;
      }

      &__about {
          font-size: 18px;
          line-height: 1.5;

          &--after {
              display: none;
              float: none;
              width: 80%;
              margin: 15px auto;
          }

          &--inline {
              display: block;
          }
      }

      &__credits {
          margin: 0 0 0 2%;
      }

      &__credit {
          line-height: 1.5;
      }

      &:after {
          content: "";
          display: table;
          clear: both;
      }
  }

  @media screen and (max-width: 700px), screen and (max-height: 400px) {
    &__body__credits{
        display: block;
        float: none;
        width: 100%;
        margin: 0;
    }
    &__body__about--inline {
        display: none;
    }
    &__body__about--after {
        display: block;
    }
  }
}
</style>
