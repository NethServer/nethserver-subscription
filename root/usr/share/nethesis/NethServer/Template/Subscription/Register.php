<?php

echo $view->header()->setAttribute('template', $T('Subscription_header'));

echo "<div id='subscriptionPlans'>";
echo "<p>". htmlspecialchars($T("subscriptions_info")) . "</p>";
echo '<div class="Buttonlist"><a id="regNowBtn" href="'.$view['PricingUrl'].'" target="_blank" title="'. htmlspecialchars($T('subscriptions_plans')) .'" role="button" aria-disabled="false">'. htmlspecialchars($T('subscriptions_plans')) .'</a></div>';
echo "<p>". htmlspecialchars($T('paste_label')) ."</p>";
echo '</div>';

echo "<div id='regForm'>";
echo $view->panel('')->insert($view->textInput('RegistrationKey', $view['SystemId'] ? $view::STATE_READONLY : ''));
echo $view->buttonList()->insert($view->button('register_now', $view::BUTTON_SUBMIT));
echo "</div>";