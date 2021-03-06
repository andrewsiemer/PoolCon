// create random client ID on pageload
var client_id = Math.random().toString(10).substring(2, 10);
// show client ID in footer
document.querySelector("#ws-id").textContent = client_id;

// establish unique websocket
var ws = new WebSocket(`ws://10.71.129.232:8000/ws/${client_id}`);

// on payload receive parse data
ws.onmessage = function(event) {
    var pool_data = JSON.parse(event.data);
    
    document.querySelector("#pool-filter").textContent = pool_data['pool-filter'];
    if (pool_data['pool-filter'] == 'ON'){
        document.getElementById("pool-filter-btn").className = 'd-sm-inline-block btn btn-sm shadow-sm btn-active';
    }
    else {
        document.getElementById("pool-filter-btn").className = 'd-sm-inline-block btn btn-sm shadow-sm';
    }
    document.querySelector("#pool-heater").textContent = pool_data['pool-heater'];
    if (pool_data['pool-heater'] == 'ON'){
        document.getElementById("pool-heater-btn").className = 'd-sm-inline-block btn btn-sm shadow-sm btn-active';
    }
    else {
        document.getElementById("pool-heater-btn").className = 'd-sm-inline-block btn btn-sm shadow-sm';
    }
    document.querySelector("#pool-temp").textContent = pool_data['pool-temp'];
    document.querySelector("#air-temp").textContent = pool_data['air-temp'];
    document.querySelector("#water-valve").textContent = pool_data['water-valve'];
    if (pool_data['water-valve'] == 'ON'){
        document.getElementById("water-valve-btn").className = 'd-sm-inline-block btn btn-sm shadow-sm btn-active';
    }
    else {
        document.getElementById("water-valve-btn").className = 'd-sm-inline-block btn btn-sm shadow-sm';
    }
    document.querySelector("#water-level").textContent = pool_data['water-level'];
    document.querySelector("#ph-level").textContent = pool_data['ph-level'];
    document.querySelector("#orp-level").textContent = pool_data['orp-level'];
};

// create interval to ask for sensor updates
var update_interval = window.setInterval(sendMessage, 1000, 'status-update');

// send event payload
function sendMessage(event) {
    ws.send(String(client_id) + ' ' + String(event))
    input.value = ''
    event.preventDefault()
}
