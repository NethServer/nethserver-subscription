<?php

echo $view->header()->setAttribute('template', $T('Subscription_header'));

$printPlanInfo = function ($label, $value) use ($T, $view) {
    if (isset($view[$value]) && $view[$value]) {
        echo "<div><span class='label'>" . htmlspecialchars($T($label)) . ": </span>";
        echo $view->textLabel($value)->setAttribute('class', 'strong');
        echo "</div>\n";
    }
};

echo "<div class='subscriptionInfo'>";
$printPlanInfo('SystemId_label', 'SystemId');
$printPlanInfo('Created_label', 'Created');
$printPlanInfo('PublicIp_label', 'PublicIp');
echo "<div style='height: 20px'></div>";
$printPlanInfo('PlanName_label', 'PlanName');
$printPlanInfo('Validity_label', 'Validity');
echo "</div>";

$view->includeJavascript("
     $('#regNowBtn').button();
");

$view->includeCss("
    #regForm {
        font-size: 120%;
    }

    #regForm h1 {
        padding: 5px;
        font-weight: bold;
    }

    #regForm p {
        padding: 10px;
        margin-bottom: 30px;
    }

    #regForm input {
        width: 64ch;
        font-family: monospace;
    }

    .subscriptionInfo {
        margin: 5px;
        padding: 5px;
        font-size: 140%;
    }

    #subscriptionPlans p {
        margin: 5px;
        font-size: 120%;
        line-height: 1.5;
        text-align: justify;
        text-justify: inter-word;
    }

    #subscriptionPlans {
        max-width: 716px;
        margin-bottom: 2em;
        padding: 8px;
        background: linear-gradient(to right, #eee, white);
        border-left: 8px solid #00719a;
    }

    .subscriptionInfo .strong {
        font-weight: bold;
    }

    #subscriptionPlans .Buttonlist {
        text-align: center;
        margin: 12px 0;
    }

    #subscriptionPlans #regNowBtn {
        color: white;
        border: 1px solid #00425b;
        text-transform: uppercase;
        background: #00719a;
    }

    div.register_spacer {
        height: 20px;
    }

    .subscriptionInfo .label {
        margin-right: 10px;
    }

");
