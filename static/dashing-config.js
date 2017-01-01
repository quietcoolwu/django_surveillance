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
  interval: 5000
});

dashboard.addWidget('buzzwords_widget', 'List', {
  getData: function () {
    $.extend(this.scope, {
      title: 'Buzzwords关键词',
      more_info: '# of times said around the office',
      updated_at: 'Last updated at 18:58',
      data: [{label: 'Exit strategy', value: 24},
        {label: 'Web 2.0', value: 15},
        {label: 'Turn-key', value: 2},
        {label: 'Enterprise', value: 12},
        {label: 'Pivoting', value: 3},
        {label: 'Leverage', value: 10},
        {label: 'Streamlininess', value: 4},
        {label: 'Paradigm shift', value: 6},
        {label: 'Synergy', value: 7}]
    });
  }
});

dashboard.addWidget('convergence_widget', 'Graph', {
  getData: function () {
    $.extend(this.scope, {
      title: 'Convergence',
      value: Math.floor(Math.random() * 50) + 40,
      more_info: '',
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

dashboard.addWidget('weather_widget', 'Weather', {
  WOEID: 2161843
});