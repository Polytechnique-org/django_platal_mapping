# coding: utf-8

from django.contrib import admin
from . import models


class SelectRelatedModelAdmin(admin.ModelAdmin):
    select_related = ()

    def queryset(self, request):
        qs = super(SelectRelatedModelAdmin, self).queryset(request)
        if self.select_related:
            qs = qs.select_related(*self.select_related)
        return qs


class SkinAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Skin, SkinAdmin)


class EmailVirtualDomainAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailVirtualDomain, EmailVirtualDomainAdmin)


class ProfileSectionEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileSectionEnum, ProfileSectionEnumAdmin)


class GeolocCountryAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GeolocCountry, GeolocCountryAdmin)


class AccountTypeAdmin(SelectRelatedModelAdmin):
    list_display = ['type', 'perms', 'description']
    search_fields = ['type', 'perms', 'description']

admin.site.register(models.AccountType, AccountTypeAdmin)


class AccountAdmin(SelectRelatedModelAdmin):
    list_display = ['uid', 'hruid', 'type', 'user_perms', 'is_admin', 'state', 'email', 'firstname', 'lastname', 'sex', 'last_version']
    list_filter = ['is_admin', 'type', 'state', 'sex', 'last_version']
    search_fields = ['firstname', 'lastname', 'email', 'full_name', 'hruid']
    select_related = ('type',)

admin.site.register(models.Account, AccountAdmin)


class ProfileAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Profile, ProfileAdmin)


class AccountProfileAdmin(SelectRelatedModelAdmin):
    list_display = ['account', 'profile', 'perms']
    search_fields = ['account__hruid', 'account__full_name', 'profile__hrpid']
    list_filter = ['perms']

admin.site.register(models.AccountProfile, AccountProfileAdmin)


class AccountAuthOpenidAdmin(SelectRelatedModelAdmin):
    select_related = ('account',)
    list_display = ['account', 'url']
    search_fields = ['account__hruid', 'url']

admin.site.register(models.AccountAuthOpenid, AccountAuthOpenidAdmin)


class AccountLostPasswordAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.AccountLostPassword, AccountLostPasswordAdmin)


class AccountXnetLostPasswordAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.AccountXnetLostPassword, AccountXnetLostPasswordAdmin)


class AnnounceAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Announce, AnnounceAdmin)


class AnnouncePhotoAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.AnnouncePhoto, AnnouncePhotoAdmin)


class AnnounceReadAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.AnnounceRead, AnnounceReadAdmin)


class EmailVirtualAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailVirtual, EmailVirtualAdmin)


class EmailRedirectAccountAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailRedirectAccount, EmailRedirectAccountAdmin)


class EmailSourceAccountAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailSourceAccount, EmailSourceAccountAdmin)


class EmailSourceOtherAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailSourceOther, EmailSourceOtherAdmin)


class EmailRedirectOtherAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailRedirectOther, EmailRedirectOtherAdmin)


class InndForumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.InndForum, InndForumAdmin)


class ForumProfileAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ForumProfile, ForumProfileAdmin)


class ForumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Forum, ForumAdmin)


class ForumSubsAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ForumSubs, ForumSubsAdmin)


class PaymentBankAccountAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PaymentBankAccount, PaymentBankAccountAdmin)


class PaymentAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Payment, PaymentAdmin)


class PaymentCodeCAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PaymentCodeC, PaymentCodeCAdmin)


class PaymentCodeRCBAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PaymentCodeRCB, PaymentCodeRCBAdmin)


class PaymentMethodAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PaymentMethod, PaymentMethodAdmin)


class PaymentReconcilationAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PaymentReconcilation, PaymentReconcilationAdmin)


class PaymentTransactionAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PaymentTransaction, PaymentTransactionAdmin)


class PaymentTransferAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PaymentTransfer, PaymentTransferAdmin)


class GroupDomAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupDom, GroupDomAdmin)


class GroupAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Group, GroupAdmin)


class GroupMemberAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupMember, GroupMemberAdmin)


class GroupMemberSubRequestAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupMemberSubRequest, GroupMemberSubRequestAdmin)


class GroupFormerMemberAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupFormerMember, GroupFormerMemberAdmin)


class GroupAnnounceAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupAnnounce, GroupAnnounceAdmin)


class GroupAnnouncePhotoAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupAnnouncePhoto, GroupAnnouncePhotoAdmin)


class GroupAnnounceReadAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupAnnounceRead, GroupAnnounceReadAdmin)


class GroupEventAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupEvent, GroupEventAdmin)


class GroupEventItemAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupEventItem, GroupEventItemAdmin)


class GroupEventParticipantAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupEventParticipant, GroupEventParticipantAdmin)


class GroupAuthAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GroupAuth, GroupAuthAdmin)


class IpWatchAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.IpWatch, IpWatchAdmin)


class LogActionAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.LogAction, LogActionAdmin)


class LogSessionAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.LogSession, LogSessionAdmin)


class LogLastSessionAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.LogLastSession, LogLastSessionAdmin)


class LogEventAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.LogEvent, LogEventAdmin)


class NewsletterAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Newsletter, NewsletterAdmin)


class NewsletterIssueAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.NewsletterIssue, NewsletterIssueAdmin)


class NewsletterCatAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.NewsletterCat, NewsletterCatAdmin)


class NewsletterArtAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.NewsletterArt, NewsletterArtAdmin)


class NewsletterInsAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.NewsletterIns, NewsletterInsAdmin)


class ProfileDisplayAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileDisplay, ProfileDisplayAdmin)


class ProfilePhoneAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfilePhone, ProfilePhoneAdmin)


class ProfilePhotoAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfilePhoto, ProfilePhotoAdmin)


class ProfilePrivateNameAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfilePrivateName, ProfilePrivateNameAdmin)


class ProfilePublicNameAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfilePublicName, ProfilePublicNameAdmin)


class ProfileAddressAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileAddress, ProfileAddressAdmin)


class ProfileAddressComponentEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileAddressComponentEnum, ProfileAddressComponentEnumAdmin)


class ProfileAddressComponentAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileAddressComponent, ProfileAddressComponentAdmin)


class ProfileBinetEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileBinetEnum, ProfileBinetEnumAdmin)


class ProfileBinetAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileBinet, ProfileBinetAdmin)


class ProfileHobbyAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileHobby, ProfileHobbyAdmin)


class ProfileNetworkingEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileNetworkingEnum, ProfileNetworkingEnumAdmin)


class ProfileNetworkingAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileNetworking, ProfileNetworkingAdmin)


class ProfileCorpsEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileCorpsEnum, ProfileCorpsEnumAdmin)


class ProfileCorpsRankEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileCorpsRankEnum, ProfileCorpsRankEnumAdmin)


class ProfileCorpsAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileCorps, ProfileCorpsAdmin)


class ProfileEducationEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileEducationEnum, ProfileEducationEnumAdmin)


class ProfileEducationDegreeEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileEducationDegreeEnum, ProfileEducationDegreeEnumAdmin)


class ProfileEducationFieldEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileEducationFieldEnum, ProfileEducationFieldEnumAdmin)


class ProfileEducationAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileEducation, ProfileEducationAdmin)


class ProfileEducationDegreeAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileEducationDegree, ProfileEducationDegreeAdmin)


class ProfileJobEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileJobEnum, ProfileJobEnumAdmin)


class ProfileJobAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileJob, ProfileJobAdmin)


class ProfileJobTermEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileJobTermEnum, ProfileJobTermEnumAdmin)


class ProfileJobTermRelationAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileJobTermRelation, ProfileJobTermRelationAdmin)


class ProfileJobTermSearchAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileJobTermSearch, ProfileJobTermSearchAdmin)


class ProfileJobTermAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileJobTerm, ProfileJobTermAdmin)


class ProfileJobEntrepriseTermAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileJobEntrepriseTerm, ProfileJobEntrepriseTermAdmin)


class ProfileLangSkillEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileLangSkillEnum, ProfileLangSkillEnumAdmin)


class ProfileLangSkillAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileLangSkill, ProfileLangSkillAdmin)


class ProfileSkillEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileSkillEnum, ProfileSkillEnumAdmin)


class ProfileSkillAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileSkill, ProfileSkillAdmin)


class ProfileMedalEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileMedalEnum, ProfileMedalEnumAdmin)


class ProfileMedalGradeEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileMedalGradeEnum, ProfileMedalGradeEnumAdmin)


class ProfileMedalAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileMedal, ProfileMedalAdmin)


class ProfileMentorAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileMentor, ProfileMentorAdmin)


class ProfileMentorCountryAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileMentorCountry, ProfileMentorCountryAdmin)


class ProfileMentorTermAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileMentorTerm, ProfileMentorTermAdmin)


class ProfilePartnersharingEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfilePartnersharingEnum, ProfilePartnersharingEnumAdmin)


class ProfilePartnersharingSettingAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfilePartnersharingSetting, ProfilePartnersharingSettingAdmin)


class ProfilePhotoTokenAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfilePhotoToken, ProfilePhotoTokenAdmin)


class ProfileMergeIssueAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileMergeIssue, ProfileMergeIssueAdmin)


class ProfileModificationAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileModification, ProfileModificationAdmin)


class ProfileVisibilityEnumAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ProfileVisibilityEnum, ProfileVisibilityEnumAdmin)


class ProfileDeltatenAdmin(SelectRelatedModelAdmin):
    raw_id_fields = ['profile']

admin.site.register(models.ProfileDeltaten, ProfileDeltatenAdmin)


class ReminderTypeAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ReminderType, ReminderTypeAdmin)


class ReminderAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Reminder, ReminderAdmin)


class ReminderTipAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.ReminderTip, ReminderTipAdmin)


class SurveyAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Survey, SurveyAdmin)


class SurveyVoteAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.SurveyVote, SurveyVoteAdmin)


class SurveyAnswerAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.SurveyAnswer, SurveyAnswerAdmin)


class GappsAccountAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GappsAccount, GappsAccountAdmin)


class GappsNicknameAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GappsNickname, GappsNicknameAdmin)


class GappsQueueAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GappsQueue, GappsQueueAdmin)


class GappsReportingAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GappsReporting, GappsReportingAdmin)


class WatchAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Watch, WatchAdmin)


class WatchGroupAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.WatchGroup, WatchGroupAdmin)


class WatchNoninsAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.WatchNonins, WatchNoninsAdmin)


class WatchProfileAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.WatchProfile, WatchProfileAdmin)


class WatchPromoAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.WatchPromo, WatchPromoAdmin)


class MxWatchAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.MxWatch, MxWatchAdmin)


class PostfixBlacklistAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PostfixBlacklist, PostfixBlacklistAdmin)


class PostfixMailseenAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PostfixMailseen, PostfixMailseenAdmin)


class PostfixWhitelistAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.PostfixWhitelist, PostfixWhitelistAdmin)


class RegisterMarketingAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.RegisterMarketing, RegisterMarketingAdmin)


class RegisterMstatAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.RegisterMstat, RegisterMstatAdmin)


class RegisterPendingAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.RegisterPending, RegisterPendingAdmin)


class RegisterPendingXnetAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.RegisterPendingXnet, RegisterPendingXnetAdmin)


class RegisterSubsAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.RegisterSubs, RegisterSubsAdmin)


class SearchAutocompleteAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.SearchAutocomplete, SearchAutocompleteAdmin)


class SearchNameAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.SearchName, SearchNameAdmin)


class RequestAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Request, RequestAdmin)


class RequestAnswerAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.RequestAnswer, RequestAnswerAdmin)


class RequestHiddenAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.RequestHidden, RequestHiddenAdmin)


class AXLetterAdmin(SelectRelatedModelAdmin):
    list_display = ['short_name', 'title', 'promo_min', 'promo_max', 'date']
    list_filter = ['bits']

admin.site.register(models.AXLetter, AXLetterAdmin)


class CarvaAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Carva, CarvaAdmin)


class ContactAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Contact, ContactAdmin)


class DowntimeAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.Downtime, DowntimeAdmin)


class EmailListModerateAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailListModerate, EmailListModerateAdmin)


class EmailSendSaveAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailSendSave, EmailSendSaveAdmin)


class EmailWatchAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.EmailWatch, EmailWatchAdmin)


class GeolocLanguageAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.GeolocLanguage, GeolocLanguageAdmin)


class HomonymListAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.HomonymList, HomonymListAdmin)


class UrlShortenerAdmin(SelectRelatedModelAdmin):
    pass

admin.site.register(models.UrlShortener, UrlShortenerAdmin)


