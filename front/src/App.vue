<template>
  <div id="app">
    <transition name="zoom" mode="out-in">
      <div key="transition-wrapper">
        <LoginButton @login-success="handleLogin" key="login-button" />
        <PlaylistCreator v-if="isLoggedIn && !playlistCreated" @playlist-created="handlePlaylistCreated" key="playlist-creator" />
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
  created() {
  const urlParams = new URLSearchParams(window.location.search);
  console.log("URL Params:", urlParams.get('loggedIn')); // Pour déboguer
  if (urlParams.get('loggedIn') === 'true') {
    this.isLoggedIn = true;
  }
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