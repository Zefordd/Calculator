var metronome = new Vue ({
    el: '#metronome',
    data: {
        start: false,
        beats_per_minute: 60,
        audio: new Audio("../../static/tick.wav"), //так ток инвалиды делают, помогите

        minutes: 10,
        seconds: 15,
    },
    methods: {
        start_metronome: function () {
            this.audio.play();
            console.log(0);
            i = 1;
            this.start = true;
            this.do_one_beat();
        },
        do_one_beat: async function () {
            while (this.start === true) {
                console.time('one_beat_time');
                this.audio.play();
                await this.sleep(60000 / this.beats_per_minute);
                console.timeEnd('one_beat_time');
            }
        },
        sleep: function (ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },

        start_timer: async function () {
            this.start = true;
            this.do_one_beat();
            while (this.minutes >= 0) {
                while (this.seconds >= 1) {
                    await this.sleep(1000);
                    this.seconds -= 1;
                }
                if (this.minutes === 0) {
                    break
                }
                this.minutes -= 1;
                this.seconds = 60;
            }
            this.start = false;
        },
    },
    delimiters: ['[[',']]']
})
