var time = -1;
function interval_timer() {
    time++;
    setTimeout("interval_timer()",50);
    postMessage(time);
};
interval_timer();