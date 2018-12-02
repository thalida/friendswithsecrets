<template>
<section
  class="thread"
  :class="[threadNameClass, selectedThreadClass]"
  v-show="isLoaded"
  v-scroll-to-session:params="{isLoaded, selectedSession: selectedSessionZeroIdx}">
  <ol class="thread__sessions container-wrapper">
    <Session
      v-for="(session, index) in threadSessions"
      :key="index"
      v-bind:index="index"
      v-bind:session="session"
      v-bind:selected="index === selectedSessionZeroIdx"
      v-on:session-toggle="onSessionToggle" />
    </ol>
</section>
</template>

<script>
import Session from './Session';

export default {
  name: 'Thread',
  components: {
    Session,
  },
  props: {
    participant: String,
    selectedSession: Number,
    isThreadSelected: Boolean,
  },
  data() {
    return {};
  },
  computed: {
    selectedSessionZeroIdx() {
      return this.selectedSession - 1;
    },
    isLoaded() {
      return this.$store.state.isLoading[this.participant] === false;
    },
    threadData() {
      return this.$store.state.threads[this.participant];
    },
    threadSessions() {
      return (this.threadData) ? this.threadData.sessions : [];
    },
    threadNameClass() {
      return `thread--${this.participant}`;
    },
    selectedThreadClass() {
      return (this.isThreadSelected) ? 'thread--selected' : '';
    },
  },
  directives: {
    scrollToSession: {
      componentUpdated(elem, args) {
        if (!args.value.isLoaded) {
          return;
        }

        const $el = elem;
        const $sessionToggle = $el.querySelector('.session__toggle');

        if ($sessionToggle === null) {
          return;
        }

        window.scrollTo(0, 0);
      },
    },
  },
  methods: {
    onSessionToggle(e) {
      this.$root.$emit('session-select', {
        participant: this.participant,
        session: (e.state === true) ? e.index : null,
      });
    },
  },
};
</script>

<style lang="scss">
@import '../assets/styles/toolkit';
.thread {
  display: block;
  position: relative;
  width: 100%;
  flex-shrink: 0;
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;

  &__sessions {
    padding: 0 0 60px 0;
  }
}

@each $person in $people {
  .thread.thread--#{$person} {
    .message--#{$person}.message--participant .message__text {
      @extend %bg-color--#{$person};
      color: $text-color-light;
    }
    .session--expanded {
      .session__toggle {
        @extend %bg-color--#{$person};
      }
    }
  }

  body.nightmode .thread.thread--#{$person} {
    .message--#{$person}.message--participant .message__text {
      background-color: $night-color-dark;
      color: $text-color-light;
    }
    .session--expanded .session__toggle {
      background-color: $night-color-dark;
    }
  }
}
</style>
