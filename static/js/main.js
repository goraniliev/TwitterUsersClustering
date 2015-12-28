/**
 * Created by goran on 12/28/15.
 */

$(document).ready(function () {
    $("#btnUpdateDatabase").click(function () {
        if (confirm('This will delete all data from your database and will insert users again. This action should' +
                ' be taken if you want to have the latest top users from time.mk. ' +
                'The insertion will take some time.')) {
            $.post('/insert_users', function () {
                alert('Database updated successfully.')
            });
        }
        else {
            alert('Database update canceled.');
        }
    });
});