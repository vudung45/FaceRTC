
'use strict';

let servers = {
    sdpSemantics: 'unified-plan'
}; //server configuration

let pc = new RTCPeerConnection({
    sdpSemantics: 'unified-plan'
});


pc.addTransceiver('video');
pc.addTransceiver('audio');

let dc = createDataChannel(); //datachannel

let dcReady = false;

const video = document.querySelector('#user-webcam');
const switchButton = document.getElementById('modeSwitch');
const subjectName = document.querySelector('#subject-name');

let registering = false;
pc.addEventListener('track', function(evt) {
	console.log("Update Stream");
    if (evt.track.kind == 'video') {
        video.srcObject = evt.streams[0];
    } 
});

function setupP2PWithServer(localOffer)
{
	return new Promise( resolve => {
		fetch("/offer",{
		body: JSON.stringify({
			sdp: localOffer.sdp,
			type: localOffer.type
		}),
		headers: 
		{
			'Content-Type': 'application/json'
		},
		method: 'POST'
		})
		.then(res => res.json())
		.then((json) =>
		{
			console.log(json);
			resolve(json);
		})
	}
	)
}

function switchMode(e)
{
	if(!registering){
		dc.send("$register$"+subjectName.value);
		registering = !registering;
		switchButton.value = "Toggle recognition mode";
	}
	else{
		dc.send("$recognize$");
		registering = !registering;
		switchButton.value = "Toggle register mode";
		
	}
}

function createDataChannel()
{

	try
	{
		let _dc = pc.createDataChannel("communication", {}); //this is a sync function
		_dc.onclose = () => console.log("Data channel `communication` closed");
	    _dc.onmessage = (event) => console.log(event.data);
	    _dc.onopen = function() {
            _dc.send("connected")
            dcReady = true;
            switchButton.addEventListener('click', e => switchMode(e));
            console.log("Data channel opened")
        };
	    return _dc;
	} catch(e)
	{
		console.log(e);
		return null;
	}
}
function setupPC(media_player)
{
	console.log("Setting up client Peer connection");
	return new Promise(resolve => {
			pc.createOffer().then((offer) => {
				return pc.setLocalDescription(offer);} //set local description
			)
			.then( () => {		
				return new Promise(function(resolve) {
		            if (pc.iceGatheringState == 'complete') {
		                resolve();
		            } else {
		                function checkState() {
		                    if (pc.iceGatheringState == 'complete') {
		                    	console.log("Local SDP setting up completed")
		                        pc.removeEventListener('icegatheringstatechange', checkState);
		                        resolve();
		                    }
		                }
		                pc.addEventListener('icegatheringstatechange', checkState);
		            }
		        }); }
			)
			.then( ()  => //now local SDP is successfully created
			{
				let localOffer = pc.localDescription;
				console.log(localOffer);
				return setupP2PWithServer(localOffer);
			}
			).then((json) => {
				console.log("Server SDP: ")
				console.log(json);
				resolve(pc.setRemoteDescription(json));
			})
	});

}


function onIceCandidate(event) {
  getOtherPc(pc).addIceCandidate(event.candidate)
    .then(
      () => onAddIceCandidateSuccess(pc),
      err => onAddIceCandidateError(pc, err)
    );
  console.log(`${getName(pc)} ICE candidate: ${event.candidate ? event.candidate.candidate : '(null)'}`);
}

function onIceStateChange(event) {
  if (pc) {
    console.log(`${getName(pc)} ICE state: ${pc.iceConnectionState}`);
    console.log('ICE state change event: ', event);
  }
}