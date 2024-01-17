<template>
  <div id="app">
    <transition name="zoom" mode="out-in">
      <div key="transition-wrapper">
        <LoginButton v-if="!isLoggedIn" @login-success="handleLogin" key="login-button" />
        <PlaylistCreator v-else-if="isLoggedIn && !playlistCreated" @genre-selected="genreSelected" @playlist-created="handlePlaylistCreated" key="genre-selector" />
        <ValidatePage v-if="playlistCreated" @return-to-creator="resetView" key="validate-page" />
      </div>
    </transition>
  </div>
</template>

<script>
import LoginButton from './components/LoginButton.vue';
import PlaylistCreator from './components/PlaylistCreator.vue';
import ValidatePage from './components/ValidatePage.vue';
export default {
  name: 'App',
  components: {
    LoginButton,
    PlaylistCreator,
    ValidatePage
  },
  data() {
    return {
      isLoggedIn: false,
      selectedGenre: null,
      playlistCreated: false
    };
  },
  methods: {
    handleLogin() {
      this.isLoggedIn = true;
    },
    genreSelected(genre) {
      this.selectedGenre = genre;
    },
    handlePlaylistCreated() {
      this.playlistCreated = true;
    },
    resetView() {
      this.playlistCreated = false;
    }
  }
}
</script>

<style>
#app {
  text-align: center;
}

.zoom-enter-active, .zoom-leave-active {
  transition: transform 0.1s;
}
.zoom-enter, .zoom-leave-to {
  transform: scale(0.3);
}
.zoom-leave-active {
  position: absolute;
}
</style>
