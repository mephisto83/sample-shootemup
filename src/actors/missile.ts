import * as ex from "excalibur";
import { Sounds, gameSheet } from "../resources";
import { Bullet } from "./bullet";

export class Missile extends ex.Actor {
    constructor() {
        super({
            pos: ex.Vector.Zero,
            width: 60,
            height: 20
        });

        this.on('precollision', this.onPreCollision);
        this.on('exitviewport', () => {
            Sounds.rocketSound.stop();
            this.kill();
        });
    }

    onInitialize(engine: ex.Engine) {
        const anim = ex.Animation.fromSpriteSheet(gameSheet, [13, 14, 15], 50, ex.AnimationStrategy.Loop);
        anim.scale = new ex.Vector(3 / 4, 3 / 4);
    }

    onPreCollision(evt: ex.PreCollisionEvent) {
        if (!(evt.other instanceof Bullet)) {
            Sounds.rocketSound.stop();
            Sounds.explodeSound.play();
            this.kill();
        }
    }
}