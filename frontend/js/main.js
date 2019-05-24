/*
Author: David Vu
Credits to a little bit of WebRTC starter

*/

'use strict';

// Put variables in global scope to make them available to the browser console.
const constraints = window.constraints = {
  audio: false,
  video: true
};



async function init(e) {


    navigator.mediaDevices.getUserMedia(constraints).then(
      (stream) =>
      {
        stream.getTracks().forEach((track) => {
          pc.addTrack(track,stream)
        })
        setupPC();
      }
    ).catch(e => console.log(e))
    
    e.target.disabled = true;
}

document.querySelector('#showVideo').addEventListener('click', e => init(e));
