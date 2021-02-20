var link = ""

chrome.browserAction.onClicked.addListener(function(activeTab){
  var newURL = "http://stackoverflow.com/";
  chrome.tabs.create({ url: newURL });
});

chrome.extension.onConnect.addListener(function(port) {
  console.log("Connected .....");
  port.onMessage.addListener(function(msg) {
       console.log("message recieved" + msg);
       port.postMessage("Hi Popup.js");
  });
})