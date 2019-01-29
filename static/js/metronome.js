Vue.component('metronome', {
    data: function () {
        return {
            audio: new Audio("../../static/Sounds/tick.wav"), 
            beats_per_minute: 60,  
        }
    },
    props: ['metronomeWork'],
    methods: {
        start_metronome: async function () {
            this.metronomeWork = true;
            this.audio.play();
            console.log(0);
            this.do_one_beat();
        },
        do_one_beat: async function () {
            while (this.metronomeWork === true) {
                console.time('one_beat_time');
                this.audio.play();
                await this.go_sleep(60000 / this.beats_per_minute);
                console.timeEnd('one_beat_time');
            }
        },
        go_sleep: function (ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },
    },
    template: '#metronome_template',
    delimiters: ['[[',']]'],
})

var metronome = new Vue ({
    el: '#metronome',
    data: {
        metronome_work: false,

    },
    methods: {

    },
    delimiters: ['[[',']]']
})
