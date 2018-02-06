var CKAN = CKAN || {};
CKAN.Templates = CKAN.Templates || {};

CKAN.Templates.resourceUpload = ' \
<div class="fileupload"> \
  <form action="http://test-ckan-net-storage.commondatastorage.googleapis.com/" class="resource-upload" \
    enctype="multipart/form-data" \
    method="POST"> \
 \
    <div class="hidden-inputs"></div> \
    <input type="file" name="file" /> \
    <br /> \
    <div class="fileinfo"></div> \
    <input id="upload" name="add-resource-upload" type="submit" class="btn btn-primary" value="'+_('Upload')+'" /> \
  </form> \
  <div class="alert alert-block" style="display: none;"></div> \
</div>';



CKAN.Templates.resourceEntry = ' \
  <li class="ui-state-default resource-edit drag-bars"> \
    <a class="resource-open-my-panel" href="#">\
      <img class="js-resource-icon inline-icon resource-icon" src="{{resource_icon}}" /> \
      <span class="js-resource-edit-name">{{resource.name}}</span>\
    </a>\
  </li>';

var youCanUseMarkdownString = 'You can use %aMarkdown formatting%b here.'.replace('%a', '<a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">').replace('%b', '</a>');
var datesAreInISOString = ('Dates are in %aISO Format%b &mdash; eg. %c2012-12-25%d or %c2010-05-31T14:30%d.').replace('%a', '<a href="http://en.wikipedia.org/wiki/ISO_8601#Calendar_dates" target="_blank">').replace('%b', '</a>').replace('%c', '<strong>').replace('%d', '</strong>');

// TODO it would be nice to unify this with the markdown editor specified in helpers.py
CKAN.Templates.resourceDetails = ' \
  <div style="display: none;" class="resource-details"> \
    <div class="flash-messages"> \
      <div class="alert alert-error resource-errors"></div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Name')+'</label> \
      <div class="controls" property="rdf:value"> \
        <input class="js-resource-edit-name" name="resources__{{num}}__name" type="text" value="{{resource.name}}" class="long" /> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+ _('Description')+'</label> \
      <div class="controls"> \
        <div class="markdown-editor"> \
          <ul class="button-row"> \
            <li><button class="btn js-markdown-edit depressed">'+_('Edit')+'</button></li> \
            <li><button class="btn js-markdown-preview">'+_('Preview')+'</button></li> \
          </ul> \
          <div> \
            <textarea class="js-resource-edit-description markdown-input" name="resources__{{num}}__description">{{resource.description}}</textarea> \
          </div> \
          <div class="markdown-preview" style="display: none;"></div> \
          <span class="hints">'+youCanUseMarkdownString+'</span> \
        </div> \
      </div> \
    </div> \
    <div class="control-group {% if resource.url_error %} error{% endif %}"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Url')+'</label> \
      <div class="controls"> \
        {% if resource.resource_type=="file.upload" %} \
          {{resource.url}} \
          <input name="resources__${num}__url" type="hidden" value="{{resource.url}}" /> \
        {% endif %} \
        {% if resource.resource_type!="file.upload" %} \
          <input name="resources__${num}__url" type="text" value="{{resource.url}}" class="long" title="{{resource.url_error}}" /> \
        {% endif %} \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Format') + '\
          &nbsp;&nbsp;<img class="js-resource-icon inline-icon resource-icon" src="{{resource_icon}}" /> </label>\
      <div class="controls"> \
        <input name="resources__{{num}}__format" type="text" value="{{resource.format}}" class="long js-resource-edit-format autocomplete-format" placeholder="'+_('e.g. csv, html, xls, rdf, ...')+'" /> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Resource Type')+'</label> \
      <div class="controls"> \
        {% if resource.resource_type=="file.upload" %} \
          '+_('Data File (Uploaded)')+' \
          <input name="resources__{{num}}__resource_type" type="hidden" value="{{resource.resource_type}}" /> \
        {% endif %} \
        {% if resource.resource_type!="file.upload" %} \
          <select name="resources__{{num}}__resource_type" class="short"> \
            {% for res in resourceTypeOptions %} \
            <option value="{{$value[0]}}" {% if $value[0]==resource.resource_type %}selected="selected"{% endif %}>{{$value[1]}}</option> \
            {% endfor %} \
          </select> \
        {% endif %} \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Last Modified')+'</label> \
      <div class="controls"> \
        <input class="input-small" name="resources__{{num}}__last_modified" type="text" value="{{resource.last_modified}}" /> \
        <div class="hint">'+datesAreInISOString+'</div> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Size (Bytes)')+'</label> \
      <div class="controls"> \
        <input name="resources__{{num}}__size" type="text" value="{{resource.size}}" class="long" /> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Mimetype')+'</label> \
      <div class="controls"> \
        <input name="resources__{{num}}__mimetype" type="text" value="{{resource.mimetype}}" /> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Mimetype (Inner)')+'</label> \
      <div class="controls"> \
        <input name="resources__{{num}}__mimetype_inner" type="text" value="{{resource.mimetype_inner}}" /> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('ID')+'</label> \
      <div class="controls"> \
        <input type="text" disabled="disabled" value="{{resource.id}}" class="disabled" /> \
        <input name="resources__{{num}}__id" type="hidden" value="{{resource.id}}" /> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Hash')+'</label> \
      <div class="controls"> \
        <input type="text" disabled="disabled" class="disabled" value="{{resource.hash or "'+_('Unknown')+'"}}"/> \
        <input name="resources__{{num}}__hash" type="hidden" value="{{resource.hash}}" /> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label for="" class="control-label" property="rdfs:label">'+_('Created')+'</label> \
      <div class="controls"> \
        <input type="text" disabled="disabled" value="{{resource.created}}" class="disabled" /> \
      </div> \
    </div> \
    <div class="control-group"> \
      <label class="control-label">'+_('Extra Fields')+' \
        <button class="btn btn-small add-resource-extra">'+_('Add Extra Field')+'</button>\
      </label>\
      <div class="controls"> \
        <div class="dynamic-extras"> \
        </div> \
      </div> \
    <button class="btn btn-danger resource-edit-delete js-resource-edit-delete">'+_('Delete Resource')+'</button>\
  </div> \
';

CKAN.Templates.resourceExtra = ' \
  <div class="dynamic-extra"> \
  <button class="btn btn-danger remove-resource-extra">X</button>\
  <input type="text" placeholder="'+_('Key')+'" class="extra-key" value="{{key}}" /> \
  <input type="text" placeholder="'+_('Value')+'" class="extra-value" value="{{value}}" /> \
  </div> \
  ';
