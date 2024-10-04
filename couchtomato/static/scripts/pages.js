var Page = {}

Page.Movie = new Class({

	Extends: PageBase,

	name: 'movie',

	initialize: function(options){

	},

	indexAction: function(param){
		var self = this
		self.getMovies()
	},
	
	getMovies: function(){
		var self = this
		this.api().request('movie', {'status': 'wanted'})
	}

})

Page.Manage = new Class({

	Extends: PageBase,

	name: 'manage',

	initialize: function(options){

	}

})

Page.Soon = new Class({

	Extends: PageBase,

	name: 'soon',

	initialize: function(options){

	}

})

Page.Config = new Class({

	Extends: PageBase,

	name: 'config',

	initialize: function(options){

	}

})

Page.Log = new Class({

	Extends: PageBase,

	name: 'log',

	initialize: function(options){

	}

})