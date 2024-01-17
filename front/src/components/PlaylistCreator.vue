<template>
  <div>
    <div class="navbar">SPOTIFY PLAYLIST CREATOR</div>
    
    <div class="genre-buttons" v-if="showPlaylistCreator">
      <button class="genre-button" v-for="genre in genres" :key="genre" @click="selectGenre(genre)">
        {{ genre }}
      </button>
      <input class="genre-input" type="text" v-model="customGenre" placeholder="Add new genre..." @keyup.enter="addCustomGenre">
    </div>
    
    <div class="playlist-creator" v-if="showPlaylistCreator && (selectedGenre || customGenre)">
      <h3>Create a Playlist for {{ selectedGenre || customGenre }}</h3>
      <input type="text" v-model="playlistName" placeholder="Enter playlist name..." class="playlist-input">
      <button @click="createPlaylist" class="create-playlist-button">Create Playlist</button>
    </div>

    <ValidatePage v-else @return-to-creator="showPlaylistCreator = true" />
  </div>
</template>

<script>
import ValidatePage from './ValidatePage.vue'

export default {
  name: 'MusicManager',
  components: {
    ValidatePage
  },
  data() {
    return {
      genres: ['Hip-Hop', 'Rock', 'Rap', 'Techno', 'Pop'],
      selectedGenre: null,
      customGenre: '',
      playlistName: '',
      showPlaylistCreator: true
    }
  },
  methods: {
    selectGenre(genre) {
      this.selectedGenre = genre;
      this.customGenre = '';
    },
    addCustomGenre() {
      if (this.customGenre.trim()) {
        this.selectedGenre = this.customGenre;
      }
    },
    createPlaylist() {
      if (this.playlistName.trim()) {
        this.$emit('playlist-created'); // Emit an event when a playlist is created
      }
  }
}
}
</script>
  <style>
  .navbar {
    background-color: #000;
    color: #fff;
    padding: 10px 0;
    font-size: 1.5em;
    text-align: center;
  }
  
  .genre-buttons {
    margin: 20px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .genre-button {
    background-color: #1DB954;
    color: white;
    border: none;
    border-radius: 20px;
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .genre-button:hover {
    background-color: #148f36;
  }
  
  .genre-input {
    margin-top: 20px;
    padding: 10px;
    border-radius: 20px;
    border: 1px solid #ccc;
    width: 80%;
  }
  
  .genre-input::placeholder {
    color: #aaa;
  }

  .playlist-creator {
  text-align: center;
  margin-top: 20px;
}

.playlist-input {
    margin-top: 20px;
    padding: 10px;
    border-radius: 20px;
    border: 1px solid #ccc;
    width: 80%;
}

.create-playlist-button {
  background-color: #1DB954;
  color: white;
  padding: 10px 20px;
  margin-top: 10px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-playlist-button:hover {
  background-color: #148f36;
}

.playlist-creator h3 {
  color: white;
  font-family: Arial, sans-serif;
}

.created-playlist-message {
  color: white;
  font-family: Arial, sans-serif;
}
  </style>
  