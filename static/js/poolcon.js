// create random client ID on pageload
var client_id = Math.random().toString(10).substring(2, 10);
// show client ID in footer
document.querySelector("#ws-id").textContent = client_id;

// establish unique websocket
var ws = new WebSocket(`ws://poolcon1.local:8000/ws/${client_id}`);

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var ctx = document.getElementById("temperaturechart");
var myLineChart = new Chart(ctx, {"type": "line", "data": {"labels": ["Data0", "Data1", "Data2", "Data3", "Data4", "Data5", "Data6", "Data7", "Data8", "Data9", "Data10", "Data11", "Data12", "Data13", "Data14", "Data15", "Data16", "Data17", "Data18", "Data19", "Data20"], "datasets": [{"label": "Numbers", "data": ["12", "12", "10", "10", "10", "9", "9", "7", "9", "9", "10", "12", "12", "16", "16", "16", "16", "16", "14", "12", "10"]}]}, "options": {"plugins": {}}});

// on payload receive parse data
ws.onmessage = function(event) {
    var pool_data = JSON.parse(event.data);
    
    document.querySelector("#pool-pump").textContent = pool_data['pool-pump'];
    if (pool_data['pool-pump'] == 'ON'){
        document.getElementById("pool-pump-btn").className = 'd-sm-inline-block btn btn-sm shadow-sm btn-active';
    }
    else {
        document.getElementById("pool-pump-btn").className = 'd-sm-inline-block btn btn-sm shadow-sm';
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
