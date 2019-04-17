//control table
var json_data, dotprobe_table;
function serverData() {
	$.ajax({
		url: "php/get.php", // this is the path to the above PHP script
		type: 'post',
		success: function (data) {
			json_data = JSON.parse(data);
			//if redirect message
			 if (json_data.redirect !== undefined && json_data.redirect){
        		// data.location contains the string URL to redirect to
				console.log('redirect true')
            	window.location.href = json_data.location;
        	} else {
				if (json_data != JSON.parse(data)){
					console.log('not equal')
					dotprobe_table = $('#database').DataTable({
						lengthMenu: [[25, 50, 100, -1], [25, 50, 100, "All"]],
						lengthChange: false,
						responsive: true,
						order: [[ 0, "desc" ]],
						dom: '<"download"B><"search"f>tp',
						buttons: ['excel', 'csv', {
							text: 'JSON',
							action: function (e, dt, button, config) {
								var data = dt.buttons.exportData();
								$.fn.dataTable.fileSave(new Blob([JSON.stringify(json_data)]),'dotprobe-js.json')
							}
            			}],
						processing: true,
						data: json_data,
						//serverSide: true,
						columns: [
							{"data": "id"},
							{"data": "code"},
							{"data": "group"}],
					});
					//dotprobe_table.buttons().container().prependTo($('#database_filter'));
					$(".download").css({"float": "left", "margin-bottom":'5px'});
					$(".search").css({"float": "right"});
					//highlight table on hover
					$('#database').on('mouseenter', 'td', function () {
						var rowIdx = dotprobe_table.cell(this).index().row;
						$(dotprobe_table.rows().nodes()).removeClass('highlight');
						$(dotprobe_table.rows(rowIdx).nodes()).addClass('highlight');
					});
				} //else {console.log('equal')};
			}
		}
	})
}
