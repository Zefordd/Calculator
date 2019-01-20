var metronome = new Vue ({
    el: '#metronome',
    data: {
        start: false,
        beats_per_minute: 60,
    },
    methods: {
        start_metronome: function () {
            console.log(0);
            i = 1;
            this.start = true;
            interval = setInterval(this.do_one_beat, 60000 / this.beats_per_minute);
        },
        do_one_beat: function () {
            console.log(i);
            if (this.start === false) {
                clearInterval(interval);
            }
            i += 1;
        },
    },
    delimiters: ['[[',']]']
})
