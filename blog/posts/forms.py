from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators, TextAreaField, SelectField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

class MultiCheckboxField(SelectMultipleField):
	widget			= ListWidget(prefix_label=False)
	option_widget	= CheckboxInput()

class AddPostForm(FlaskForm): 
    title = StringField('Blog Title', validators=[DataRequired()])
    body = PageDownField('Blog Body', validators=[DataRequired()])
    category = MultiCheckboxField('Existing Category', choices=[('1','jav'), ('2', 'hentai')])
    new_category = StringField('Add Category, separated by comma')
    submit = SubmitField('Add Post')

class UpdatePostForm(FlaskForm): 
    title = StringField('Blog Title', validators=[DataRequired()] )
    body = TextAreaField('Blog Body', validators=[DataRequired()])
    submit = SubmitField('Update Post')

class AddCommentForm(FlaskForm): 
    content = PageDownField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

