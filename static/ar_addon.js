/* eslint-disable no-undef */

AFRAME.registerComponent('look-at-id', {
	schema: { target: { type: 'string' } },

	init: function () {},

	tick: function () {
		if (typeof this.data === 'string') {
			const elem = document.getElementById(this.data);
			if (elem !== null) this.data = elem;
			else return;
		}
		this.el.object3D.lookAt(this.data.object3D.position);
	}
});

console.log('addons loaded');
