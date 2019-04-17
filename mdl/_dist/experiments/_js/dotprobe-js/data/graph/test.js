// Transpose the data into layers
//https://github.com/d3/d3-shape/blob/master/README.md#stacks
////////////////////////////////////////////////////////////////////////////////////////////
filter_json = _.filter(json_data, {subject_subsession: 'abc'});//filter
temp_array = Object.keys(temp_keys).reverse();


var tt;
var data = d3.layout.stack()([0,1,2,3,4,5].map(function (score) {
		return filter_json.map(function (d) {
			subject_id = d['subject_id'];
			return {
				//x: d['session_number'],
				subject_id: d['score']
				//session: d['session_id'],
				//subject: d['subject_id']
			};
		});
	})
);

////////////////////////////////////////////////////////////////////////////////////////////
filter_json = _.filter(json_data, {subject_subsession: 'abc'});//filter
temp_array = Object.keys(temp_keys).reverse();


// Transpose the data into layers
//var tt;
//var data = _.chain(filter_json)
//    //.map('subject_session')
//	.flatten()
//    .keyBy('subject_session')
//    .mapValues(function(val) {
//		tt = val
//        return _.omit(val.score, 'subject_id');
//    })
//    .value(); 

//var tt;
//var data = _.flatMap(filter_json, function (obj) {
//	tt = obj
//	return _.map(obj.subject_session, function (param) {
//		return {
//			name: obj.name,
//			session: obj.subsession
//		};
//	});
//});

//function update(arr, key, newval, name, score, session) {
//	match = _.find(arr, key);
//	if (!match){
//	_.merge(match, {[name]: score});
//	} else {
//		arr[session].push({[name]: score});
//	}
//};


function update(arr, subject, score, session) {
	if (!arr[session]){
		arr[session] = []
		_.merge(arr[session], {[subject]: score});
	} else {
		_.merge(arr[session], {[subject]: score});
	}
};



temp[session] = {}

_.merge(temp[0], {'semeon': score});

////////////////////////////////////////////////////////////////////////////////////////////testing here-------------
// array = []
// object = {}
//map
//transform
//Transpose
/////////////////
filter_json = _.filter(json_data, {subject_subsession: 'abc'});//filter
temp_array = Object.keys(temp_keys).reverse();
