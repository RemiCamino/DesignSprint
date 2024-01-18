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
import axios from 'axios';

export default {
  name: 'PlaylistCreator',
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
  if (this.playlistName.trim() && (this.selectedGenre || this.customGenre)) {
    axios.post('http://localhost:5000/create_playlist', {
      genre: this.selectedGenre || this.customGenre,
      playlist_name: this.playlistName
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log(response.data);
      this.$emit('playlist-created');
    })
    .catch(error => {
      console.error('Error creating playlist:', error);
    });
  }
}

}
}
</script>
  <style>
.navbar {
  background-color: #000;
  color: #fff;
  padding: 15px 0;
  font-size: 2em;
  text-align: center;
  font-family: 'Helvetica Neue', sans-serif; 
  letter-spacing: 1px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
  margin-left: 10px;
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
  