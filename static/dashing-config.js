/**
 * Created by wukai on 12/31/16.
 */

/* global Dashboard */

let dashboard = new Dashboard();

dashboard.addWidget('clock_widget', 'Clock');

dashboard.addWidget('new_users_widget', 'Number', {
  getData: function () {
    let self = this;
    Dashing.utils.get('new_users_widget', function (scope) {
      $.extend(self.scope, scope);
    });
  },
  interval: 3017
});

dashboard.addWidget('plc_data_widget', 'List', {
  getData: function () {
    let self = this;
    Dashing.utils.get('plc_data_widget', function (scope) {
      $.extend(self.scope, scope);
    });
  },
  interval: 2000
});

dashboard.addWidget('convergence_widget', 'Graph', {
  getData: function () {
    $.extend(this.scope, {
      title: '当前累计报警数',
      value: Math.floor(Math.random() * 50) + 40,
      more_info: 'test',
      data: [
        {x: 0, y: Math.floor(Math.random() * 50) + 40},
        {x: 1, y: Math.floor(Math.random() * 50) + 40},
        {x: 2, y: Math.floor(Math.random() * 50) + 40},
        {x: 3, y: Math.floor(Math.random() * 50) + 40},
        {x: 4, y: Math.floor(Math.random() * 50) + 40}
      ]
    });
  }
});
