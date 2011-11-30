from django.contrib import comments
from django.contrib.comments import signals
from django.contrib.comments.views.comments import CommentPostBadRequest, comment_done
from django.contrib.comments.views.utils import next_redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import escape
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from CommentRecaptcha.forms import RecaptchaForm

@csrf_protect
@require_POST
def verify_comment(request, next=None, using=None):
    """
    Verify a comment. A ReCaptcha will be shown for verification.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.username
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Check to see if the POST data overrides the view's next argument.
    next = data.get("next", next)

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except TypeError:
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % \
                escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % \
                (escape(ctype), escape(object_pk)))
    except (ValueError, ValidationError), e:
        return CommentPostBadRequest(
            "Attempting go get content-type %r and object PK %r exists raised %s" % \
                (escape(ctype), escape(object_pk), e.__class__.__name__))

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = comments.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    # If there are errors or if we requested a preview show the comment
    if form.errors or preview:
        template_list = [
            # These first two exist for purely historical reasons.
            # Django v1.0 and v1.1 allowed the underscore format for
            # preview templates, so we have to preserve that format.
            "comments/%s_%s_preview.html" % (model._meta.app_label, model._meta.module_name),
            "comments/%s_preview.html" % model._meta.app_label,
            # Now the usual directory based template heirarchy.
            "comments/%s/%s/preview.html" % (model._meta.app_label, model._meta.module_name),
            "comments/%s/preview.html" % model._meta.app_label,
            "comments/preview.html",
        ]
        return render_to_response(
            template_list, {
                "comment" : form.data.get("comment", ""),
                "form" : form,
                "next": next,
            },
            RequestContext(request, {})
        )
    template_list = [
            "comments/%s_%s_verify.html" % (model._meta.app_label, model._meta.module_name),
            "comments/%s_verify.html" % model._meta.app_label,
            "comments/%s/%s/verify.html" % (model._meta.app_label, model._meta.module_name),
            "comments/%s/verify.html" % model._meta.app_label,
            "comments/verify.html",
        ]
    request.session['data'] = request.POST.copy()
    request.session['model'] = models.get_model(*ctype.split(".", 1))
    request.session['target'] = model._default_manager.using(using).get(pk=object_pk)
    return render_to_response(
        template_list, {
            "comment" : form.data.get("comment", ""),
            "form" : RecaptchaForm(),
            "next": next,
        }, RequestContext(request, {}))

@csrf_protect
@require_POST
def post_comment(request, next=None, using=None):
    form = RecaptchaForm(request.POST)
    data = request.session['data']
    model = request.session['model']
    target = request.session['target']
    next = data.get("next", next)
    if form.is_valid():
        form = comments.get_form()(target, data=data)
        comment = form.get_comment_object()
        comment.ip_address = request.META.get("REMOTE_ADDR", None)
        if request.user.is_authenticated():
            comment.user = request.user

        # Signal that the comment is about to be saved
        responses = signals.comment_will_be_posted.send(
            sender  = comment.__class__,
            comment = comment,
            request = request
        )

        for (receiver, response) in responses:
            if response == False:
                return CommentPostBadRequest(
                    "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)

        # Save the comment and signal that it was saved
        comment.save()
        signals.comment_was_posted.send(
            sender  = comment.__class__,
            comment = comment,
            request = request
        )
        return next_redirect(data, next, comment_done, c=comment._get_pk_val())
    else:
        template_list = [
            "comments/%s_%s_verify.html" % (model._meta.app_label, model._meta.module_name),
            "comments/%s_verify.html" % model._meta.app_label,
            "comments/%s/%s/verify.html" % (model._meta.app_label, model._meta.module_name),
            "comments/%s/verify.html" % model._meta.app_label,
            "comments/verify.html",
        ]
        return render_to_response(
            template_list, {
                "comment" : request.session['data'].get("comment", ""),
                "form" : form,
                "next": next,
            }, RequestContext(request, {}))
