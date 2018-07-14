<template>
    <div>
        <header class="header">
            <div class="header__bar">
                <router-link to="/" class="header__link">threadsss</router-link>
                <span class="header__btn" v-on:click="toggle()">
                    <span v-if="!headerIsOpen">?</span>
                    <span v-else>X</span>
                </span>
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
                        for inquires email us at <a href="#">threadsss@gmail.com</a>
                    </p>
                </div>
            </div>
        </header>
        <p class="header__body__about header__body__about--after" v-if="location === 'home'">
            Three friends participated in 15 individual online text therapy
            sessions from January to April 2018. These sessions capture a slice
            of their life, their thoughts and feelings, their individualitiies,
            and how they try to process the world around them. The identities of
            the therapists have been protected.
        </p>
    </div>
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
  methods: {
    toggle() {
      this.headerIsOpen = !this.headerIsOpen;
    },
  },
};
</script>

<style lang="scss" scoped>
.header {
    display: block;
    position: relative;
    width: 100%;
    height: auto;
    padding: 15px 0;
    background: linear-gradient(#79E2F7, #1DE5EB);

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
            color: #222222;
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

    @media screen and (max-width: 700px) {
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

