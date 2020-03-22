$(function()
{
    new Def.Autocompleter.Search('condition',
      'https://clinicaltables.nlm.nih.gov/api/conditions/v3/search');

    new Def.Autocompleter.Search('condition2',
        'https://clinicaltables.nlm.nih.gov/api/conditions/v3/search');

    $(document.forms["inclusion-form"]).on('click', '.btn-add', function(e)
    {
        e.preventDefault();

        var controlForm = $('.controls form:first'),
            currentEntry = $(this).parents('.entry:first'),
            newEntry = $(currentEntry.clone()).appendTo(controlForm);

        newEntry.find('input').val('');
        controlForm.find('.entry:not(:last) .btn-add')
            .removeClass('btn-add').addClass('btn-remove').removeClass('fa-plus')
            .html('<i class="fas fa-minus fa-lg btn-remove" style="#FF6347"></i>');
    }).on('click', '.btn-remove', function(e)
    {
		$(this).parents('.entry:first').remove();

		e.preventDefault();
		return false;
	});

    $(document.forms["exclusion-form"]).on('click', '.btn-add', function(e)
    {
        e.preventDefault();

        var controlForm = $('.controls form:last'),
            currentEntry = $(this).parents('.entry:first'),
            newEntry = $(currentEntry.clone()).appendTo(controlForm);

        newEntry.find('input').val('');
        controlForm.find('.entry:not(:last) .btn-add')
        .removeClass('btn-add').addClass('btn-remove').removeClass('fa-plus')
        .html('<i class="fas fa-minus fa-lg btn-remove" style="#FF6347"></i>');
    }).on('click', '.btn-remove', function(e)
    {
		$(this).parents('.entry:first').remove();

		e.preventDefault();
		return false;
	});
});
