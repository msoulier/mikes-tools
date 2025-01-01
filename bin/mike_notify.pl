#!/usr/bin/perl

use strict;
use Net::SMTP;
our $VERSION;
our %IRSSI;

use Irssi;
use Gtk2::Notify -init, "Irssi";

$VERSION = '1.0';
%IRSSI = (
    authors     => 'Michael P. Soulier',
    contact     => 'msoulier@digitaltorque.ca',
    name        => 'Notify Mike',
    description => 'This script is a custom notification script ' .
                   'for notifying me when someone is trying to ' .
                   'get my attention.',
    license     => 'Public Domain',
);

my $notify_desktop = 1;
my $send_email = 1;
my $debug = 1;

sub debug {
    my $text = shift;
    Irssi::print($text)
        if $debug;
}

sub notify_desktop {
    my ($nick, $msg, $privpub) = @_;
    $msg =~ s/<|>/ /g;
    $privpub =~ s/ally$//;
    $privpub =~ s/ly$//;
    my $summary = "$privpub MSG from $nick in IRC";
    my $notification = Gtk2::Notify->new($summary, $msg);
    $notification->show;
}

sub send_email {
    my ($nick, $msg, $privpub) = @_;
    #my @toaddrs = ('msoulier@digitaltorque.ca', 'michael_soulier@mitel.com');
    my @toaddrs = ('msoulier@digitaltorque.ca');
    my $fromaddr = 'do-not-reply@digitaltorque.ca';

    my $conn = Net::SMTP->new('localhost');
    debug("connecting to smtp server at localhost");
    $conn->mail($fromaddr);
    $conn->recipient(@toaddrs);
    $conn->data();
    my $toaddrs = join ',', @toaddrs;
    my $data =<<EOF;
To: $toaddrs
From: $fromaddr
Subject: Notice in IRC

$nick msged you $privpub.

---begin quote---
$msg
---end quote---
EOF
    $conn->datasend($data);
    $conn->quit();
    debug("done sending");
}

sub notify {
    send_email(@_)
        if $send_email;
    notify_desktop(@_)
        if $notify_desktop;
}

sub sig_message_public {
     my ($server, $msg, $nick, $nick_addr, $target) = @_;
     notify($nick, $msg, 'publically')
        if $msg =~ /msoulier/;
}

sub sig_message_private {
     my ($server, $msg, $nick, $nick_addr) = @_;
     debug("received private message from $nick");
     notify($nick, $msg, 'privately');
}

Irssi::signal_add 'message public', 'sig_message_public';
Irssi::signal_add 'message private', 'sig_message_private';
