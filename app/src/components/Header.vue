<template>
  <header class="header">
      <div class="header__bar">
          <a
            tabindex="0"
            class="header__btn"
            v-on:click="toggle()"
            v-on:keyup.enter="toggle()"
            :title="(headerIsOpen ? 'Close' : 'Open') + ' about section'">
              <span v-if="!headerIsOpen">?</span>
              <span v-else>X</span>
          </a>
      </div>
      <transition name="animation-fade-height">
          <div class="header__body container-wrapper" v-if="headerIsOpen">
              <p class="header__body__about">
                Three friends from different backgrounds participated in 10
                individual online text therapy sessions from January to April 2018.
                Friends With Secrets captures a slice of their lives
                — the good and the bad — including identity, feelings,
                and how they try to process the world around them.
                The identities of the therapists have been protected.
              </p>
              <div class="header__body__credits">
                  <p class="header__body__credit">
                    Project by
                    <a href="https://twitter.com/AkilahObviously" target="_blank">Akilah Hughes</a>,
                    <a href="https://twitter.com/robynkanner">Robyn Kanner</a>,
                    and <a href="https://www.instagram.com/timothygoodman/">Timothy Goodman</a>
                  </p>
                  <p class="header__body__credit">
                    Design by
                    <a href="https://twitter.com/robynkanner">Robyn Kanner</a>
                    and <a href="https://www.instagram.com/timothygoodman/">Timothy Goodman</a>
                  </p>
                  <p class="header__body__credit">
                    Code by <a href="http://thalida.codes/">Thalida Noel</a>
                  </p>
                  <p class="header__body__credit">
                    For inquires email us at
                    <a mailto="friendswithsecrets@gmail.com">friendswithsecrets@gmail.com</a>
                  </p>
              </div>
          </div>
      </transition>
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
  padding: 0;
  transition: background-color 400ms ease;

  &__bar {
      display: block;
      margin: 0 auto;
      width: 100%;

      &:after {
          content: "";
          clear: both;
          display: table;
      }
  }

  &__btn {
      display: inline-block;
      float: right;
      width: 30px;
      margin: 15px;
      padding: 5px 0;
      cursor: pointer;
      border-radius: 50%;
      background: #FFFFFF;
      text-align: center;
  }

  &__body {
      position: relative;
      height: auto;

      a {
          color: $text-color;
      }

      &__about,
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

  @media screen and (max-width: 700px), screen and (max-height: 400px) {
    &__body__about,
    &__body__credits {
        display: block;
        float: none;
        width: 100%;
        margin: 0 0 20px 0;
    }
  }
}
</style>
