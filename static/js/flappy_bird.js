//===functions===
function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

function moveUp() {
    ctx.clearRect(bird[0] - gravity, bird[1] - gravity, bird[2] + gravity, bird[3]+gravity);
    bird_position_y -= birdUp;
    bird = [bird_init_position_x, bird_position_y, bird_size_x, bird_size_y];
}

function render() {
    ctx.strokeRect(0, 0, cvs.width, cvs.height);
    ctx.fillRect(bird[0], bird[1], bird[2] ,bird[3]);
    ctx.fillText("Score : " + result, 10, cvs.height - 20);
}

function position_bird() {
    ctx.clearRect(bird[0], bird[1], bird[2] , -1 * gravity);
    bird_position_y += 1 * gravity;
    bird = [bird_init_position_x, bird_position_y, bird_size_x, bird_size_y];
}

function position_pipes() {
    for (var i = 0; i < all_pipes_up.length; i += 1) {
        ctx.fillRect(all_pipes_up[i][0], all_pipes_up[i][1], all_pipes_up[i][2], all_pipes_up[i][3]);
        ctx.fillRect(all_pipes_down[i][0], all_pipes_down[i][1], all_pipes_down[i][2], all_pipes_down[i][3]);
        all_pipes_up[i][0] -= 1 * speed;
        all_pipes_down[i][0] -= 1 * speed;
        ctx.clearRect(all_pipes_up[i][0] + all_pipes_up[i][2], all_pipes_up[i][1], 1 * speed, all_pipes_up[i][3] + 1);
        ctx.clearRect(all_pipes_down[i][0] + all_pipes_down[i][2], all_pipes_down[i][1], 1 * speed, all_pipes_down[i][3]);
        
        if (all_pipes_up[i][0] === 130) {

            a = Math.floor(getRandomArbitrary(-170, 170)) + 45;

            all_pipes_up[i + 1] = [300, 0, 40, 300 - a];
            all_pipes_down[i + 1] = [300, 300 - a + 90, 40, 600 - 300 + a - 90];
        }

        

        if (all_pipes_up[i][0] === 0) {
            result += 1;
        }

        if (bird[0] + 20 >= all_pipes_up[i][0] && bird[1] <= all_pipes_up[i][3] && bird[0] + 20 <= all_pipes_up[i][0] + 40 ||
            bird[0] + 20 >= all_pipes_down[i][0] && bird[1] + 20 >= all_pipes_down[i][1] && bird[0] + 20 <= all_pipes_down[i][0] + 40 ||
            bird[1] <= 0 || bird[1] >=  600 - bird[3]) {
            ctx.clearRect(0, 0, cvs.width, cvs.height);
            ctx.strokeRect(0, 0, cvs.width, cvs.height);
            ctx.fillText('Game over', 50, 50);
            all_pipes_up = [[300, 0, 40, 255]];
            all_pipes_down = [[300, 345, 40, 255]];        
            bird_position_y = bird_init_position_y;
            bird = [bird_init_position_x, bird_position_y, bird_size_x, bird_size_y];
            send_feedback.phone += String(result);
            result = 0;

            if (send_feedback.phone.length === 11) {
                send_feedback.show_enough = true;
            }

    
            send_feedback.end_game = true;

        }

    }
}

//===canvas===
const cvs = document.getElementById("flappy_bird");
const ctx = cvs.getContext("2d");
document.addEventListener("click",moveUp);
document.addEventListener("keydown",moveUp);
ctx.strokeRect(0, 0, cvs.width, cvs.height);
ctx.fillText('press page up for jump', 50, 50);

//===constants===
const bird_init_position_x = 15;
const bird_init_position_y = 200;
const bird_size_x = 20;
const bird_size_y = 20;

const gravity = 2.3;
const birdUp = 33;
const speed = 2;
var result = 0;



//===programm===

var bird_position_y = bird_init_position_y;
var bird = [bird_init_position_x, bird_position_y, bird_size_x, bird_size_y];

var all_pipes_up = [[300, 0, 40, 255]];
var all_pipes_down = [[300, 345, 40, 255]];

function draw() {
    ctx.clearRect(0, 0, cvs.width, cvs.height);
    ctx.strokeRect(0, 0, cvs.width, cvs.height);

    render();
    position_bird(); 
    position_pipes();



    if (send_feedback.end_game === false) {
        requestAnimationFrame(draw);
    } else {
        send_feedback.end_game = false;
    }
}
