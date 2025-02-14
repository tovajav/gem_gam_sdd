
var cmsCore = {

    mobile: 767, /* surchargeable localement */
    tablet: 1024, /* surchargeable localement */

    init: function () {
        'use strict';

        // gestion title lien externe/document
        $(' a.external, a.document').each(function () {
            let title = $(this).attr('title');
            if (title === undefined) {
                title = $(this).clone();
                $('[aria-hidden="true"]', title).remove();
                title = title.text().trim();
                if (title === '') {
                    var $img = $('img', $(this));
                    if ($img.length) {
                        title = $img.attr('alt').trim();
                    }
                }
            }
            if (title !== '') {
                if ($(this).hasClass('external')) {
                    title += ' (nouvelle fenêtre)';
                } else if ($(this).data('file_ext') !== undefined) {
                    let cplt = ' (' + $(this).data('file_ext');
                    if ($(this).data('file_weight') !== undefined) {
                        cplt += ' - ' + $(this).data('file_weight');
                    }
                    cplt += ')';
                    title += cplt;
                    $(this).append(cplt);
                }
                $(this).attr('title', title.replace(/\s+/g, ' '));
            }
        });

        // Toggle ARIA
        cmsCore.ariaInit($(document));

        // Défilement progessif au clic sur une ancre
        $(document).on('click', 'a[href^=\'#\']', function () {
            if (!$(this).hasClass('noScroll')) {
                cmsCore.scroll($($(this).attr('href')));
                return false;
            }
            return true;
        });

        //colorbox
        $('a.lightbox').colorbox({
            title: function () {
                return $(this).data('title') !== '' ? $(this).data('title') : ' ';
            },
            onComplete: function () {
                var alt = '';
                if ($('img', this).attr('alt') !== $(this).data('title') && $('img', this).attr('alt') !== '') {
                    alt = $('img', this).attr('alt');
                }
                $('.cboxPhoto').attr('alt', alt);
            },
            maxWidth: '95%',
            maxHeight: '95%'
        });

        // credit image
        $('.spanCredit').hide();
        $('.spanImgOuter').attr('tabindex', 0)
            .hover(
                function () {
                    $('.spanCredit', this).fadeIn();
                },
                function () {
                    $('.spanCredit', this).fadeOut();
                }
            )
            .on('focus', function () {
                $('.spanCredit', this).fadeIn();
            })
            .on('blur', function () {
                $('.spanCredit', this).fadeOut();
            });

        // Traitement rédactionnel
        $('.txt table:not(\'.tableNotResponsive\'), .partage table:not(\'.tableNotResponsive\'), .tpl table:not(\'.tableNotResponsive\')').wrap('<div class="tableauContainer"/>');

        // Lien d'évitement
        $('#lienEvitement').find('a')
            .on('focus', function () {
                $(this).closest('#lienEvitement').addClass('focus');
            })
            .on('blur', function () {
                $(this).closest('#lienEvitement').removeClass('focus');
            })
            .on('click', function () {
                if ($(this).hasClass('triggerClick')) {
                    if ($(this).data('controls')) {
                        var $e = $('#' + $(this).data('controls'));
                        if ($e.is(':visible')) {
                            $e.trigger('click', [true]);
                            return false;
                        }
                    } else {
                        $($(this).attr('href')).trigger('click', [true]);
                        return false;
                    }
                }
                return true;
            });

        // Haut de page sticky
        var $hautDePage = $('#hautDePage');
        $hautDePage.hide();
        $(document).scroll(function () {
            if ($(window).scrollTop() > 1) {
                $hautDePage.show(400);
            } else {
                $hautDePage.hide(400);
            }
        });

        // Google tracker pour les liens document + externe
        $(document).on('click', 'a.document', function () {
            window.open(this.href);
            return false;
        });
        $(document).on('click', 'a.external', function () {
            window.open(this.href);
            return false;
        });

        //gestion nb caractère max
        $('textarea[data-maxchar], input[data-maxchar]')
            .each(function () {
                $(this).attr('aria-describedby', $(this).attr('id') + '_max');
                $(this).after('<span class="counter" id="' + $(this).attr('id') + '_max' + '"></span>');
            })
            .on('keyup', function () {
                var $span = $(this).nextAll('span.counter');
                $span.html('Nombre de caractères : ' + $(this).val().length + ' / ' + $(this).data('maxchar'));
                if ($(this).val().length > $(this).data('maxchar')) {
                    $span.css('color', 'red');
                } else {
                    $span.css('color', '');
                }
            })
            .keyup();

        //confirm
        $(document).on('click', '.confirm', function () {
            var str = 'Êtes-vous sûr';
            if ($(this).attr('title') !== undefined && $(this).attr('title') !== '') {
                str += ' de vouloir\n"' + $(this).attr('title') + '"';
            }
            str += ' ?';
            return confirm(str);
        });

        // gestion CB required
        $('div[data-required-cb], span[data-required-cb]').each(function () {
            var $cCB = $('input[type="checkbox"]', $(this));
            var nb = $(this).data('required-cb');
            $cCB.on('change', function () {
                if ($cCB.filter(':checked').length >= nb) {
                    $cCB.each(function () {
                        this.setCustomValidity('');
                        $(this).prop('required', false);
                    });
                } else {
                    $cCB.filter(':not(:checked)').each(function () {
                        this.setCustomValidity('Veuillez cocher au moins ' + nb + ' option(s)');
                    });

                }
            });
            if ($cCB.filter(':checked').length < $(this).data('required-cb')) {
                $cCB.filter(':not(:checked)').prop('required', true);
            }
        });

        //type d'input
        $.datepicker.setDefaults($.datepicker.regional["fr"]);
        $('input[data-type="date"]')
            .attr('placeholder', 'jj/mm/aaaa')
            .attr('title', 'Format attendu : 01/01/2021')
            .attr('pattern', '^(((0[1-9]|[12]\\d|3[01])/(0[13578]|1[02])/((19|[2-9]\\d)\\d{2}))|((0[1-9]|[12]\\d|30)/(0[13456789]|1[012])/((19|[2-9]\\d)\\d{2}))|((0[1-9]|1\\d|2[0-8])/02/((19|[2-9]\\d)\\d{2}))|(29/02/((1[6-9]|[2-9]\\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))))$')
            .attr('maxlength', '10')
            .not('.noCalendar')
            .datepicker({
                changeMonth: true,
                changeYear: true
            });
        $('input[data-type="telephone"]')
            .attr('pattern', '^0[1-9][0-9]{8}$')
            .attr('title', 'Format attendu : 0142535433');
        $('input[data-type="integer"]')
            .attr('pattern', '^[0-9]*$')
            .attr('title', 'Format attendu : nombre entier')
            .addClass('alignright');
        $('input[data-type="float"]')
            .attr('pattern', '^[0-9]*\.?[0-9]*$')
            .attr('title', 'Format attendu : nombre décimal')
            .addClass('alignright');
        //gestion de l'étoile
        $('input[required], select[required], textarea[required]').not('input:checkbox, input:radio')
            .each(function () {
                $('label[for="' + $(this).attr('id') + '"]', $(this).closest('form')).append(' <span class="obligatoire">*</span>');
            });
        $('input[required][type="checkbox"], input[required][type="radio"], div[data-required-cb], span[data-required-cb]').closest('p').find('label:first').append(' <span class="obligatoire">*</span>');
        //formatage virgule flottante
        $(document).on('keyup', 'input[data-type="float"]', function () {
            $(this).val($(this).val().replace(/,/, '.'));
        });
        //formatage espace sur nombre
        $(document).on('keyup', 'input[data-type="float"], input[data-type="integer"]', function () {
            $(this).val($(this).val().replace(/\s/, ''));
        });
        //formatage caractère sur téléphone
        $(document).on('keyup', 'input[data-type="telephone"]', function () {
            $(this).val($(this).val().replace(/\D/, ''));
        });

        // Lecteur audio multi HTML5
        (function () {
            var current = 0;
            var autoplay = true;

            // Pour chaque lecteur
            $('.audioPlayerMulti').each(function (i, player) {
                player = $(player);
                var audio = player.find('audio');
                var playlist = player.find('.playlist');
                var tracks = playlist.find('li a');

                // Première piste active
                tracks.eq(0).parent().addClass('active');

                // Choix des pistes
                tracks.click(function (e) {
                    var $track = $(this);
                    var li = $track.parent();

                    e.preventDefault();

                    // Remplacement des sources
                    audio.find('source').remove();
                    var audioProperties = $track.data('audioProperties');
                    audio.append('<source type="audio/mp3" src="' + $track.attr('href') + '">');
                    if (audioProperties[0].srcOgg) {
                        audio.append('<source type="audio/ogg" src="' + audioProperties[0].srcOgg + '">');
                    }
                    // Remplacement de l'alternative HTML
                    audio.children('.htmlAlternative').html(audioProperties[0].htmlAlternative);

                    // Changement de la piste active
                    li.addClass('active').siblings().removeClass('active');

                    // Reload et lecture de la piste
                    audio[0].load();
                    audio[0].play();

                    // Nouvelle piste en cours
                    current = li.index();
                });

                // Piste suivante
                audio.on('ended', function () {
                    if (autoplay) {
                        current = current >= tracks.length - 1 ? 0 : current + 1;
                        tracks.eq(current).trigger('click');
                    }
                });
            });
        })();
    },
    ariaInit: function ($root) {
        $('.aria-toggle', $root)
            .on('click', function (e) {
                const $button = $(this);
                const $target = $('#' + $button.attr('aria-controls'));
                if ($button.attr('aria-expanded') === 'true') {
                    // on ferme
                    $target
                        .attr('aria-hidden', 'true')
                        .slideUp(function () {
                            $button.attr('aria-expanded', 'false');
                        })
                        .off('keydown.aria.' + $button.attr('id'));
                    $('body').off('click.aria.' + $button.attr('id'));
                    $button.focus();
                } else {
                    // on ouvre
                    $target.removeAttr('aria-hidden').slideDown();
                    $button.attr('aria-expanded', 'true');
                    // on focus (au besoin seulement)
                    if ($button.data('focus') === true) {
                        $target.focus();
                        if (!$target.is(':focus')) {
                            $target.attr('tabindex', '-1');
                            $target.focus();
                        }
                    }
                    // echappe
                    $target.on('keydown.aria.' + $button.attr('id'), function (ev) {
                        if (ev.which === 27) {
                            $button.trigger('click', [true]);
                        }
                    });
                    // clic en dehors
                    $('body').on('click.aria.' + $button.attr('id'), function (ev, triggered) {
                        if (!triggered && !$(ev.target).closest($button).length && !$(ev.target).closest($target).length) {
                            $button.trigger('click', [true]);
                        }
                    });
                }
                e.preventDefault();
            })
            .on('keydown', function (e) {
                if (e.which === 32) {
                    $(this).trigger('click', [true]);
                    return false;
                }
            });
        $('.aria-close', $root).on('click', function (e) {
            $('#' + $(this).attr('aria-controls')).trigger('click', [true]);
            e.preventDefault();
        });
    },
    scroll: function ($idtf, delta, noFocus) {
        if ($idtf.length > 0) {
            if (!delta) {
                delta = 0;
            }
            $('html, body').animate({scrollTop: $idtf.offset().top + delta}, 'fast');
            if (!noFocus) {
                $idtf.focus();
                if (!$idtf.is(':focus')) {
                    $idtf.attr('tabindex', '-1');
                    $idtf.focus();
                }
            }
        }
    }
};
$(cmsCore.init);

//legende image, Doit être executé après le chargement des images
$(window).load(function () {
    'use strict';
    $('.spanImgContainer').width(function () {
        var $img = $('.spanImgOuter img', $(this)).outerWidth();
        var $parent = $(this).closest('.innerParagraphe').width();
        if ($img > $parent) {
            return $parent;
        }
        return $img;
    });
});

/*
 * PRISE EN CHARGE DES BULLES D'AIDE SUR LES FORMULAIRES
 * jQuery accessible simple (non-modal) tooltip window, using ARIA
 * Adaptation de https://a11y.nicolas-hoffmann.net/simple-tooltip/
 * License MIT: https://github.com/nico3333fr/jquery-accessible-simple-tooltip-aria/blob/master/LICENSE
 */
(function () {

    'use strict';

    /*
     * jQuery accessible simple (non-modal) tooltip window, using ARIA
     * @version v2.2.0
     * Website: https://a11y.nicolas-hoffmann.net/simple-tooltip/
     * License MIT: https://github.com/nico3333fr/jquery-accessible-simple-tooltip-aria/blob/master/LICENSE
     */

    function accessibleSimpleTooltipAria(options) {
        var element = $(this);
        options = options || element.data();
        var text = options.simpletooltipText || '';
        var prefix_class = typeof options.simpletooltipPrefixClass !== 'undefined' ? options.simpletooltipPrefixClass + '-' : '';
        var content_id = typeof options.simpletooltipContentId !== 'undefined' ? '#' + options.simpletooltipContentId : '';

        var index_lisible = Math.random().toString(32).slice(2, 12);
        var aria_describedby = element.attr('aria-describedby') || '';

        element.attr({
            'aria-describedby': 'label_simpletooltip_' + index_lisible + ' ' + aria_describedby
        });

        if (element.parents('label').attr('for')) {
            var $field = $('#' + $(this).parents('label').attr('for'));
            var helper_id = element.attr('id') ? element.attr('id') : 'helper_' + index_lisible;
            element.attr('id', helper_id);
            var aria_describedby = $field.attr('aria-describedby') || '';
            $field.attr({
                'aria-describedby': element.attr('id') + ' ' + aria_describedby
            });
        }

        element.wrap('<span class="' + prefix_class + 'simpletooltip_container"></span>');

        var html = '<span class="js-simpletooltip ' + prefix_class + 'simpletooltip" id="label_simpletooltip_' + index_lisible + '" role="tooltip" aria-hidden="true">';

        if (text !== '') {
            html += '' + text + '';
        } else {
            var $contentId = $(content_id);
            if (content_id !== '' && $contentId.length) {
                html += $contentId.html();
            }
        }
        html += '</span>';

        $(html).insertAfter(element);
    }

    // Bind as a jQuery plugin
    $.fn.accessibleSimpleTooltipAria = accessibleSimpleTooltipAria;

    $(function () {
        $('.helper').each(function () {
            var map = {
                '&': '&amp;',
                '\'': '&#39;',
                '"': '&quot;',
                '<': '&lt;',
                '>': '&gt;'
            };
            $(this).replaceWith('<span tabindex="0" class="js-simple-tooltip helper" data-simpletooltip-text="' + $(this).html().replace(/[&"'\<\>]/g, function (c) {
                return map[c];
            }) + '"><img src="' + SIT_IMAGE + 'tooltip.png" alt="Aide contextuelle"></span>');
        });
        $('.js-simple-tooltip')
            .each(function () {
                // Call the function with this as the current tooltip
                accessibleSimpleTooltipAria.apply(this);
            });

        // events ------------------
        $('body')
            .on('mouseenter focusin', '.js-simple-tooltip', function () {
                var $this = $(this);
                var aria_describedby = $this.attr('aria-describedby');
                var tooltip_to_show_id = aria_describedby.substr(0, aria_describedby.indexOf(' '));
                var $tooltip_to_show = $('#' + tooltip_to_show_id);
                $tooltip_to_show.attr('aria-hidden', 'false');
            })
            .on('mouseleave', '.js-simple-tooltip', function (event) {
                var $this = $(this);
                var aria_describedby = $this.attr('aria-describedby');
                var tooltip_to_show_id = aria_describedby.substr(0, aria_describedby.indexOf(' '));
                var $tooltip_to_show = $('#' + tooltip_to_show_id);
                var $is_target_hovered = $tooltip_to_show.is(':hover');

                if (!$is_target_hovered) {
                    $tooltip_to_show.attr('aria-hidden', 'true');
                }
            })
            .on('focusout', '.js-simple-tooltip', function (event) {
                var $this = $(this);
                var aria_describedby = $this.attr('aria-describedby');
                var tooltip_to_show_id = aria_describedby.substr(0, aria_describedby.indexOf(' '));
                var $tooltip_to_show = $('#' + tooltip_to_show_id);

                $tooltip_to_show.attr('aria-hidden', 'true');
            })
            .on('mouseleave', '.js-simpletooltip', function () {
                var $this = $(this);
                $this.attr('aria-hidden', 'true');
            })
            .on('keydown', '.js-simple-tooltip', function (event) {
                // close esc key

                var $this = $(this);
                var aria_describedby = $this.attr('aria-describedby');
                var tooltip_to_show_id = aria_describedby.substr(0, aria_describedby.indexOf(' '));
                var $tooltip_to_show = $('#' + tooltip_to_show_id);

                if (event.keyCode == 27) { // esc
                    $tooltip_to_show.attr('aria-hidden', 'true');
                }
            });
    });
})();
