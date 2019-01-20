var metronome = new Vue ({
    el: '#metronome',
    data: {
        start: false,
        beats_per_minute: 60,
        audio: new Audio("../../static/tick.wav"), //так ток инвалиды делают, помогите
    },
    methods: {
        start_metronome: function () {
            console.log(this.audio);
            this.audio.play();
            console.log(0);
            i = 1;
            this.start = true;
            interval = setInterval(this.do_one_beat, 60000 / this.beats_per_minute);
        },
        do_one_beat: function () {
            console.log(i);
            this.audio.play();
            if (this.start === false) {
                clearInterval(interval);
            }
            i += 1;
        },
    },
    delimiters: ['[[',']]']
})
