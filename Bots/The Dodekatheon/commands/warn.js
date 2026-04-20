const { SlashCommandBuilder, EmbedBuilder, PermissionFlagsBits } = require('discord.js'); //Importing libraries. What is PermissionFlagBits?
/* [It is a giant list of all Discord permissions (like Administrator, ManageMessages, etc.). 
You use it if you want to lock a command so that only people with certain permissions can even see it in their menu.]*/
const db = require('../../db'); //Bath to my database.js
require('dotenv').config(); //Why do we need an .env here?

module.exports = {
    data: new SlashCommandBuilder()
    .setName('warn')
    .setDescription('Issue a warning to a member')
    .addUserOption(option => 
        option
        .setName('member')
        .setDescription('The member to warn')
        .setRequired(true) 
        )
    .addStringOption(option => 
        option
        .setName('reason')
        .setDescription('Reason for the warning')
        .setRequired(true)
        )
    .addStringOption(option =>
        option
        .setName('link')
        .setDescription('Link to the offending message')
        .setRequired(false)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence1')
        .setDescription('Evidence Attachment 1')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence2')
        .setDescription('Evidence Attachment 2')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence3')
        .setDescription('Evidence Attachment 3')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence4')
        .setDescription('Evidence Attachment 4')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence5')
        .setDescription('Evidence Attachment 5')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence6')
        .setDescription('Evidence Attachment 6')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence7')
        .setDescription('Evidence Attachment 7')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence8')
        .setDescription('Evidence Attachment 8')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence9')
        .setDescription('Evidence Attachment 9')
        .setRequired(true)
    )
    .addAttachmentOption(option => 
        option
        .setName('evidence10')
        .setDescription('Evidence Attachment 10')
        .setRequired(true)
    ),

    async execute(interaction){
        //Checking if this person is a mod manually, make it dynamic through the settings database later
        const ModRoleID = "1073396088603693167"
        if(!interaction.member.roles.cache.has(ModRoleID)) {
            return interaction.reply({
                content: "❌ Only the Council of Elders can issue warnings.",
                ephemeral: true
            });
        }
        await interaction.deferReply({
            ephemeral: true
        });
        const target = interaction.options.getUser('member');
        const reason = interaction.options.getString('reason');
        const messageLink = interaction.options.getString('link') || "No link provided";

        //Evidence Gathering
        const evidence = []
        for (let i=1; i<=2; i++) {
            const attachment = interaction.options.getAttachment(`evidence${i}`);
            if (attachment) {
                evidence.push(attachment.url);
            }
        }

        try {
            //Database Logging, replacing old json logging
            //We'll store this in the warnings table of the database
            const SQL = `
            INSERT INTO themis.warnings("userID", "moderatorID", "reason", "evidence", "messageLink", "timestamp")
            VALUES($1, $2, $3, $4, $5, NOW())
            `;
            await db.query(SQL, [target.id, interaction.user.id, reason, evidence, messageLink]);

            //Logging Embed. What does it do? [It's just the fancy formatted box (the EmbedBuilder) that gets sent to your private staff channels. 
            // It makes the data readable at a glance instead of just being plain text.]
            const unixTimestamp = Math.floor(Date.now() / 1000);
            const LogEmbed = new EmbedBuilder()
                .setTitle("⚖️ Warning Logged")
                .setColor(0xFFA500) //Orange
                .addFields(
                    {
                        name: "Handled By:",
                        value: `${interaction.user}`,
                        inline: false //What does inline mean?? [If inline true then Discord will try to put the fields side by side.
                    },                // If false then it gets it's own full line (like a stack)]
                    {
                        name: "Member Warned",
                        value: `${target} (${target.id})`,
                        inline: false
                    },
                    {
                        name: "Reason",
                        value: reason,
                        inline: false
                    },
                    {
                        name: "Evidence",
                        value: evidence.join('\n') || "None",
                        inline: false
                    }
                )
                .setFooter({
                    text: "This warning has been logged by Themis."
                })
                .setTimestamp();

                //Send to log channels, remember to put them in my settings table
                const logChannelIDs = [
                    process.env.mainLogChannelID,
                    process.env.modLogChannelID
                ];

                for (const id of logChannelIDs) {
                    const channel = await interaction.client.channels.fetch(id).catch(() => null);
                    if (channel) await channel.send({
                        embeds: [LogEmbed]
                    });
                }
                await interaction.editReply(`✅ ${target.tag} has been warned.`)
        } catch (err) {
            console.error(err);
            await interaction.editReply("⚠️ Failed to log warning in the database.");
        }
    
    }
    
};